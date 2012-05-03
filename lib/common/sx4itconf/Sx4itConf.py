import ConfigParser
import os

class UsageException(BaseException):
  """
  This exception is thrown when the server.conf file is invalid.
  You can print the message to get more informations.
  """
  def __init__(self, key):
    self.key = key
  def __str__(self):
    return "No %s used, check your server.conf or your command line."%str(self.key)

class ArgsAndFileParser:
  """
  A simple config file parser, that allow to override the config with command line options.
  """
  def __init__(self, configFile):
    self.opts = {}
    config = ConfigParser.RawConfigParser()
    config.read(configFile)
    self.loadItemsFromSection(config, "server")
    self.loadItemsFromSection(config, "controller")
    self.loadItemsFromSection(config, "database")
  def __str__(self):
    return str(self.opts)
  def __getitem__(self, key):
    if self.opts.get(key) is None:
      raise UsageException(key)
    return self.opts.get(key)
  def addArgsParser(self, parser):
    """
    You can override the file option by giving an **optparse** object.
    """
    (options, args) = parser.parse_args()
    opt = options.__dict__
    for b in opt:
      if opt[b] is not None:
        self.opts[b] = opt[b]
  def loadItemsFromSection(self, config, section):
    d = {}
    if not config.has_section(section):
      return
    for b in config.items(section):
      d[section + "_" + b[0]] = b[1]
    self.opts = dict(self.opts.items() + d.items())

opts = ArgsAndFileParser(os.path.expanduser('~/.4am.conf'))
