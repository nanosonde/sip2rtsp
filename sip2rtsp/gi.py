import sys
import textwrap

try:
    import gi

    gi.require_version("Gst", "1.0")
    from gi.repository import GLib, GObject, Gst
except ImportError:
    print(
        textwrap.dedent(
            """
        ERROR: A GObject based library was not found.
        GStreamer is required. GStreamer is a C library with a
        number of dependencies itself, and cannot be installed with the regular
        Python tools like pip.
    """
        )
    )
    raise
else:
    Gst.init([])
    gi.require_version("GstApp", "1.0")
    gi.require_version("GstPbutils", "1.0")
    gi.require_version('GstRtsp', '1.0')
    gi.require_version('GstRtspServer', '1.0')
        
    from gi.repository import GstApp
    from gi.repository import GstPbutils
    from gi.repository import GstRtsp
    from gi.repository import GstRtspServer

GLib.set_prgname("sip2rtsp")
GLib.set_application_name("sip2rtsp")

REQUIRED_GST_VERSION = (1, 21, 3)
REQUIRED_GST_VERSION_DISPLAY = ".".join(map(str, REQUIRED_GST_VERSION))

if Gst.version() < REQUIRED_GST_VERSION:
    sys.exit(
        f"ERROR: GStreamer >= {REQUIRED_GST_VERSION_DISPLAY} required, "
        f"but found {Gst.version_string()}."
    )


__all__ = [
    "GLib",
    "GObject",
    "Gst",
    "GstRtsp",
    "GstRtspServer",
    "GstApp",
    "GstPbutils",
    "gi",
]
