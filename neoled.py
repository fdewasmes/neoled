#!/usr/bin/env python
from rgbmatrix import RGBMatrix
from cyrusbus import Bus
import time, sys, json, pprint, logging, logging.config
from apscheduler.schedulers.background import BackgroundScheduler
from webserver import webserver
import argparse
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

logging.config.fileConfig(dir_path + '/logging.conf')
# create logger
neologger = logging.getLogger('neoled')


class NeoLed():
    def callback(self, bus, argument):
        self.called_bus = bus

        self.default_layout = int(argument)
        self.matrix.Clear()

    def __init__(self, *args, **kwargs):
        self.bus = Bus()

        parser = argparse.ArgumentParser(description='Fuel your RGB Matrix with useful informations')
        parser.add_argument('-f', type=str,
                            help='the config file to use', dest='config_file', default='./sample-config/config.json')
        args = parser.parse_args()
        self.config_file = args.config_file

        self.load_config()
        self.init_matrix()
        self.webserver = webserver(self.bus)
        self.default_layout = 0
        # prepare scheduler
        self.scheduler = BackgroundScheduler()

    def load_config(self):
        with open(self.config_file, 'r') as f:
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
            self.scheduler.shutdown()
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
        self.scheduler.start()
        self.webserver.start()
        widget_instances = []

        for layout in self.config["layouts"]:
            widget_instances.append(self.__load_widgets_for_layout(layout))

        neologger.info("= loading providers")
        for provider in self.config["providers"]:
            neologger.info("\tcreating " + provider["type"])
            provider_class = self.get_class(provider["type"])
            provider_instance = provider_class(self.bus, **provider)
            self.scheduler.add_job(provider_instance.run, 'interval', seconds=provider["refreshInterval"])

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

        if self.config["defaultLayout"] is not None:
            self.default_layout = self.config["defaultLayout"]

        self.bus.subscribe("layout.event", self.callback)

        if self.default_layout < len(widget_instances):
            while True:
                if self.default_layout < len(widget_instances):
                    for widget in widget_instances[self.default_layout]:
                        widget.Display()
                    self.matrix.SwapOnVSync(self.offscreenCanvas)
                    time.sleep(0.1)

    def __load_widgets_for_layout(self, layout_file):
        neologger.info("= loading widgets for layout file " + layout_file)
        with open(dir_path + "/" + layout_file, 'r') as f:
            layout = json.load(f)
        widgets = []
        for widget in layout:
            neologger.info("\tcreating " + widget["type"])
            widget_class = self.get_class(widget["type"])
            widget_instance = widget_class(self.matrix, self.bus, self.offscreenCanvas, **widget)
            widgets.append(widget_instance)
        return widgets

# Main function
if __name__ == "__main__":
    # start neoled
    neoled = NeoLed()
    neoled.run()
