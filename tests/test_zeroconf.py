
from pytest import raises

from mopidy.internal.process import exit_process
from mopidy import zeroconf
from mopidy.zeroconf import _convert_text_list_to_dbus_format, _is_loopback_address

# dbus is None, and therefore an AttributeError is raised
def test_convert_text():
    with raises(AttributeError):
        _convert_text_list_to_dbus_format(["aString"])
        
# The third parameter is the port, and should be an integer, not a string
def test_port_as_string():
    zeroConf = zeroconf.Zeroconf(1, 2, "portString")
    with raises(TypeError):
        zeroConf.__str__()

# The 5th parameter is the host, which should be a string. Therefore an AttrubuteError
# should be thrown when passing an int 
def test_check_publish():
    zeroConf = zeroconf.Zeroconf(1, 2, 3, "", 2)
    with raises(AttributeError):
            zeroConf.publish()
