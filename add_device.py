import tango
dev_info = tango.DbDevInfo()
dev_info.server = "nmdev/transformer01"
dev_info._class = "nmdev"
dev_info.name = "transformer01/nmdev/transformer"
db = tango.Database()
db.add_device(dev_info)
print("[OK] Device added to database")