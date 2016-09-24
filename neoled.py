#!/usr/bin/env python
from rgbmatrix import RGBMatrix
from cyrusbus import Bus
import time, sys, json, pprint, logging, logging.config
from apscheduler.schedulers.background import BackgroundScheduler
from webserver import webserver


logging.config.fileConfig('logging.conf')
# create logger
neologger = logging.getLogger('neoled')


class NeoLed():
    def __init__(self, *args, **kwargs):
        self.bus = Bus()
        self.load_config()
        self.init_matrix()
        self.webserver = webserver(self.bus)

    def load_config(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)

    def init_matrix(self):
        self.matrix = RGBMatrix(self.config["matrix"]["rows"], self.config["matrix"]["chain"],
                                self.config["matrix"]["parallel"])
        self.matrix.pwmBits = self.config["matrix"]["pwmbits"]
        self.matrix.brightness = self.config["matrix"]["brightness"]
        self.offscreenCanvas = self.matrix.CreateFrameCanvas()

    def run(self):
        logging.getLogger().info("starting")
        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.start()
        except KeyboardInterrupt:
            print("Exiting\n")
            scheduler.shutdown()
            self.webserver.stop()
            sys.exit(0)

    def get_class(self, kls):
        parts = kls.split('.')
        if (len(parts) > 1):
            module = ".".join(parts[:-1])
            m = __import__(module)
            for comp in parts[1:]:
                m = getattr(m, comp)
        else:
            thismodule = sys.modules[__name__]
            m = getattr(thismodule, kls)
        return m

    def start(self):

        self.webserver.start()
        widget_instances = []

        neologger.info("= loading widgets")
        for widget in self.config["widgets"]:
            neologger.info("\tcreating " + widget["type"])
            widget_class = self.get_class(widget["type"])
            widget_instance = widget_class(self.matrix, self.bus, self.offscreenCanvas, **widget)
            widget_instances.append(widget_instance)

        neologger.info("= loading providers")
        for provider in self.config["providers"]:
            neologger.info("\tcreating " + provider["type"])
            provider_class = self.get_class(provider["type"])
            provider_instance = provider_class(self.bus, **provider)
            scheduler.add_job(provider_instance.run, 'interval', seconds=provider["refreshInterval"])

        neologger.info("= loading adapters")
        for adapter in self.config["adapters"]:
            neologger.info("\tcreating " + adapter["type"])
            adapter_class = self.get_class(adapter["type"])
            adapter_instance = adapter_class(self.bus, **adapter)

        neologger.info("= loading commands")
        for command in self.config["commands"]:
            neologger.info("\tcreating " + command["type"])
            command_class = self.get_class(command["type"])
            command_instance = command_class(self.bus, **command)

        neologger.info("Bus state:\n" + pprint.pformat(self.bus.subscriptions))

        while True:
            for widget in widget_instances:
                widget.Display()
            self.matrix.SwapOnVSync(self.offscreenCanvas)
            time.sleep(0.1)

# Main function
if __name__ == "__main__":
    # prepare scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()

    # start neoled
    neoled = NeoLed()
    neoled.run()
