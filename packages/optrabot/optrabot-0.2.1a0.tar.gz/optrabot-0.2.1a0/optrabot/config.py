"""
Module to define the config of the application
"""
from collections import UserDict
from ruyaml import YAML
from ruyaml.scanner import ScannerError
from loguru import logger
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import NumberValidator
from InquirerPy.validator import EmptyInputValidator

import os
import sys

configFileName = "config.yaml"
defaultHubHost = 'http://tradinghub.quantx.gmbh'

class Config(UserDict):
	def __init__(self, config_path=configFileName):
		self.config_path = os.path.expanduser(config_path)
		self.load()

	def load(self):
		"""
        Loads configuration from configuration YAML file.
        """
		logger.debug("Try loading config file...")
		try:
			with open(os.path.expanduser(self.config_path), 'r') as f:
				try:
					self.data = YAML().load(f)
					logger.debug("Config loaded successfully.")
				except ScannerError as e:
					logger.error("Error parsing yaml of configuration file '{}' :{}", e.problem_mark, e.problem)
		except FileNotFoundError:
			logger.error(
				 "Error opening configuration file {}".format(self.config_path)
			)
			self.createDefaultConfig()

	def createDefaultConfig(self):
		""" Create a default configuration 
		"""
		logger.info('Using a default configuration.')
		defaultDoc = 'general:\n'
		defaultDoc += '  agentid: testagent\n'
		self.data = YAML().load(defaultDoc)

	def get(self, key):
		"""
		Fetch the configuration value for the specified key. If there are nested dictionaries, a dot
		notation can be used.

		So if the configuration contents are:

		self.data = {
			'first': {
				'second': 'value'
			},
		}

        self.data.get('first.second') == 'value'

		Arguments:
        	key(str): Configuration key to fetch
		"""
		keys = key.split('.')
		value = self.data.copy()

		for key in keys:
			value = value[key]

		return value
	
	def save(self):
		"""
		Saves configuration in the configuration YAML file.
		"""
		with open(os.path.expanduser(self.config_path), 'w+') as f:
			yaml = YAML()
			yaml.default_flow_style = False
			yaml.dump(self.data, f)

def ensureInitialConfig() -> bool:
	configPath = os.path.expanduser(configFileName)
	if os.path.exists(configPath):
		return True
	print("No config.yaml found. Let's answer some questions and generate the required configuration file.")
	configOK = False
	try:
		confAPIKey = inquirer.text(message="What's your OptraBot API Key:").execute()
		confAgentId = inquirer.text(message="Give your OptraBot Instance an Id:", default="optrabot").execute()
		confWebPort = inquirer.number(message="Port number on which the OptraBot UI will be accessible:", default=8080).execute()
		confTWSHost = inquirer.text(message="Hostname of your TWS/IB Gateway machine:",default="127.0.0.1").execute()
		confTWSPort = inquirer.number(message="Port number of your TWS/IB Gateway:",default=7496, validate=NumberValidator()).execute()
		confTWSClientID = inquirer.number(message="Client ID to be used for TWS/IB Gateway connection:",default=21, validate=NumberValidator()).execute()
		confTWSMarketData = inquirer.select(
			message="Select a market data type:",
			choices=[
	            "Live",
	            "Delayed",
	            #Choice(value=None, name="Exit"),
	        ],
	        default="Live",
		).execute()
		confTradingAccount = inquirer.text(message="Account number to be used for trading:",default="").execute()
		confTradingContracts = inquirer.number(message="Number of IronFly contracts to be traded:", min_allowed=1).execute()
		confTradingPriceIncement = inquirer.number(message="Increment for limit price adjustments ($):",default=0.1, float_allowed=True, validate=EmptyInputValidator()).execute()
		confTradingMinimumPremium = inquirer.number(message="Minimum premium for an Iron Fly trade ($):",default=14, float_allowed=True, validate=EmptyInputValidator()).execute()
		confTradingTakeProfit = inquirer.number(message="Percentage of captured premium as profit target (%):", default=8, min_allowed=1, max_allowed=100).execute()
		confTradingStopLoss = inquirer.number(message="Percentage of captured premium as stop loss level (%):", default=16, min_allowed=1).execute()
		confirm = inquirer.confirm(message="Confirm?", default=True).execute()
	except KeyboardInterrupt as exc:
		print('Configuration has been aborted!')
		return False

	if not confirm:
		print("Configuration assistant abortet!")
		return

	data = dict(general=dict(port=confWebPort, apikey=confAPIKey, agentid=confAgentId, hub=defaultHubHost),
				tws=dict(host=confTWSHost, port=int(confTWSPort), clientid=int(confTWSClientID), marketdata=confTWSMarketData, 
			 			account=confTradingAccount, contracts=int(confTradingContracts), adjustmentstep=float(confTradingPriceIncement), minimumPremium=float(confTradingMinimumPremium), takeprofit=int(confTradingTakeProfit), stoploss=int(confTradingStopLoss))
			 )
	configYAML = yaml=YAML()
	try:
		with open(configFileName, 'w') as configFile:
			configYAML.dump(data, configFile )
		print("Config file " + configFileName + " has been generated based on your answers.\nYou may modify the configuration file manually if required.")
		configOK = True
	except IOError as exc:
		print("Error generating the config file:", configFileName)
		print("I/O error({0}): {1}".format(exc.errno, exc.strerror))
		return
	
	return configOK