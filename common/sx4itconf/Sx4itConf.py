import ConfigParser

class UsageException(BaseException):
  def __init__(self, key):
    self.key = key
  def __str__(self):
    return "No %s used, check your server.conf or your command line."%str(self.key)

class ArgsAndFileParser(object):
  def __init__(self):
    self.opts = {}
    config = ConfigParser.RawConfigParser()
    config.read("server.conf")
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

opts = ArgsAndFileParser()
