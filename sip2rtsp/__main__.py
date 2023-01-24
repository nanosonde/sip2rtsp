import faulthandler

faulthandler.enable()

from sip2rtsp.gi import GLib  # noqa: F401

import threading
import signal
import asyncio
import logging

from sip2rtsp.app import Sip2RtspApp

threading.current_thread().name = "sip2rtsp"

logger = logging.getLogger(__name__)


async def shutdown(signal, loop, glib_loop, glib_thread):

    logging.info(f"Received exit signal {signal.name}...")

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]

    logging.debug(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

    if glib_thread and glib_loop:
        # Now handle the GLib main loop
        logger.debug(f"Quitting glib main loop...")
        glib_loop.quit()
        logger.debug(f"Done.")
        logger.debug(f"Joining glib main loop thread...")
        glib_thread.join()
        logger.debug(f"Done.")
        glib_loop = None
        glib_thread = None


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.set_debug(False)

    glib_loop = GLib.MainLoop()
    glib_thread = threading.Thread(target=glib_loop.run)
    glib_thread.start()

    sip2rtsp_app = Sip2RtspApp(loop, glib_loop)

    async def graceful_shutdown(s, loop, glib_loop, glib_thread):
        await sip2rtsp_app.stop()
        await shutdown(s, loop, glib_loop, glib_thread)

    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s,
            lambda s=s: asyncio.create_task(
                graceful_shutdown(s, loop, glib_loop, glib_thread)
            ),
        )

    main_task = loop.create_task(sip2rtsp_app.start())

    try:
        asyncio.set_event_loop(loop)
        logger.debug(f"Entering loop.run_forever()...")
        loop.run_forever()
        logger.debug(f"Left loop.run_forever()...")
    except KeyboardInterrupt:  # pragma: no branch
        logger.debug(f"Received KeyboardInterrupt")
    finally:
        loop.run_until_complete(main_task)
        loop.close()
        asyncio.set_event_loop(None)

    logger.debug(f"main() exit...")
