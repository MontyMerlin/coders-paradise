import remi.gui as gui
import time, sys, io, threading, random
import numpy as np
from remi import start, App
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot



class MatplotImage(gui.Image):

    def __init__(self, **kwargs):
        super(MatplotImage, self).__init__("/%s/get_image_data?update_index=0" % id(self), **kwargs)
        self._buf = None
        self._buflock = threading.Lock()
       
        
        self.redraw(0)

    def redraw(self,months):
        fig = plot
        fig.gcf().clear()
        # Get x values of the sine wave
        times = np.arange(months-3, months+7, 0.1)
        # Amplitude of the sine wave is sine of a variable like time
        amplitude = np.sin(times)
        # Plot a sine wave using time and amplitude obtained for the sine wave
        fig.plot(times, amplitude)
        # Give a title for the sine wave plot
        fig.title('Market analysis')
        # Give x axis label for the sine wave plot
        fig.xlabel('Months')
        # Give y axis label for the sine wave plot
        fig.ylabel("Potential profits")
        fig.grid(True, which='both')
        fig.axhline(y = 0 , color='k')
        fig.axvline(x = months, color="red")

        buf = io.BytesIO()
        plot.savefig(buf, format='png')
        with self._buflock:
            if self._buf is not None:
                self._buf.close()
            self._buf = buf

        i = int(time.time() * 1e6)
        self.attributes['src'] = "/%s/get_image_data?update_index=%d" % (id(self), i)

        super(MatplotImage, self).redraw()
        
    def get_image_data(self, update_index):
        with self._buflock:
            if self._buf is None:
                return None
            self._buf.seek(0)
            data = self._buf.read()

        return [data, {'Content-type': 'image/png'}]

class A_humble_startup(App):

    def __init__(self, *args):

        margins = "10px auto"
        button_width = "30%"
        button_height = "30"

        # container widgets
        self.master_container = gui.VBox(width='100%', height='100%')
        self.lower_container = gui.HBox(width="100%", height="70%")
        self.upper_buttons = gui.HBox(width='100%', height='15%')
        self.lower_buttons = gui.HBox(width='100%', height='15%')
        self.labels_container  = gui.VBox(width='50%', height='90%')
        self.lower_container.append(self.labels_container,1)
        self.master_container.append([self.upper_buttons,self.lower_buttons, self.lower_container])

        # trackers
        self.hire_cost = 100
        self.profitability = 300000
        self.lines_of_code = 0
        self.last_passive = 0
        self.last_increment = 0
        self.rate = 0
        self.number_of_coders = 0
        self.funds = 5000
        self.assets = 0
        self.shippable = False

        # time controlls
        self.months = 0
        self.last_month = 0
        self.time_dilation = 20 # seconds per month
        # coder outputs 5 lines of code per second 
        self.rate = 0.2 # seconds per line of code (this aso govrns the rate at which the number ticks over)

        # availabel funds label
        self.funds_label = gui.Label("Available funds: £" + str(self.funds), margin=margins, style = {"font-weight": "bold"})
        self.labels_container.append(self.funds_label,1)       

        # lines of code label
        self.count_lable = gui.Label("Lines of code written: " + str(self.lines_of_code), margin=margins, style = {"font-weight": "bold"})
        self.labels_container.append(self.count_lable,2)

        #number of coders label
        self.coder_label = gui.Label("code minions: " + str(self.number_of_coders), margin=margins, style = {"visibility":"hidden","font-weight": "bold"})
        self.labels_container.append(self.coder_label,3)

        #project month label
        self.month_label = gui.Label("Project month: " + str(self.months), margin=margins, style = {"font-weight": "bold"})
        self.labels_container.append(self.month_label,0)

        #Assets label
        self.asset_label = gui.Label("Invested assets: " + str(self.assets), margin=margins, style = {"visibility":"hidden","font-weight": "bold"})
        self.labels_container.append(self.asset_label,4)

        # exit button
        self.exit_button = gui.Button('Quit',width = button_width, height = button_height, margin=margins)
        self.exit_button.onclick.connect(self.Exit)
        self.upper_buttons.append(self.exit_button, 0)

        # self.hire_button new coders button
        self.hire_button = gui.Button('Hire a programmer for £{} / month'.format(self.hire_cost),width = button_width, height = button_height, margin=margins, style = {"visibility":"hidden"})
        self.hire_button.onclick.connect(self.Hire)
        self.upper_buttons.append(self.hire_button, 2)

        # self.write_button some code button
        self.write_button = gui.Button('Write some code!',width = button_width, height = button_height , margin=margins)
        self.write_button.onclick.connect(self.Write)
        self.upper_buttons.append(self.write_button, 1)

        #invest
        self.invest_button = gui.Button('Invest £1000 for a 3% monthly ROI',width = button_width, height = button_height , margin=margins, style = {"visibility":"hidden"})
        self.invest_button.onclick.connect(self.Invest)
        self.lower_buttons.append(self.invest_button, 2)

        #ship your app button
        self.ship_button = gui.Button('Ship your app for £{}'.format(self.profitability),width = button_width, height = button_height , margin=margins, style = {"visibility":"hidden"})
        self.ship_button.onclick.connect(self.Ship)
        self.lower_buttons.append(self.ship_button,1)

        #fire button
        self.fire_button = gui.Button('Fire a programmer',width = button_width, height = button_height , margin=margins, style = {"visibility":"hidden"})
        self.fire_button.onclick.connect(self.Fire)
        self.lower_buttons.append(self.fire_button,0)

        # matplotlib graph
        self.mpl = MatplotImage(width=400, height=400)
        self.lower_container.append(self.mpl,0)

        # required, for Start class input
        super(A_humble_startup, self).__init__(*args)
        
    def Exit(self,button):
        # cleanly exit the app
        print("Exiting...")
        self.close()
        sys.exit()

    def Write(self,button): 
        # self.write_button code and update label
        self.lines_of_code += 1
        self.count_lable.set_text("Lines of code written " + str(self.lines_of_code))

        if self.lines_of_code == 10:
            self.hire_button.style.update({"visibility":"visible"})
            self.coder_label.style.update({"visibility":"visible"})

    def Ship(self,button):
        self.shippable = False
        self.ship_button.style.update({"visibility":"hidden"})
        self.invest_button.style.update({"visibility":"visible"})
        self.asset_label.style.update({"visibility":"visible"})
        self.funds += self.profitability
        self.funds_label.set_text("Available funds: £" + str(self.funds))
        self.lines_of_code = 0
        self.count_lable.set_text("Lines of code written " + str(self.lines_of_code))

    def Invest(self,button):
        self.funds -= 1000
        self.funds_label.set_text("Available funds: £" + str(self.funds))
        self.assets += 1
        self.asset_label.set_text("Invested assets: " + str(self.assets))

    def Fire(self,button):
        self.number_of_coders -= 1
        self.coder_label.set_text("Code minions: " + str(self.number_of_coders))
        if self.number_of_coders <= 0:
            self.fire_button.style.update({"visibility":"hidden"})

    def Hire(self,button):
        # self.hire_button a new coder and update label
        self.number_of_coders += 1
        self.coder_label.set_text("Code minions: " + str(self.number_of_coders))
        self.fire_button.style.update({"visibility":"visible"})


    def idle(self):
        # this method is run before every GUI update call
        if self.number_of_coders > 0:
            if (time.perf_counter() - self.last_increment) > self.rate:
                self.last_increment = time.perf_counter()
                self.lines_of_code += self.number_of_coders
                self.count_lable.set_text("Lines of code written " + str(self.lines_of_code))

        # track months
        if (time.perf_counter() - self.last_month) > self.time_dilation:
            self.last_month = time.perf_counter()
            self.months += 1
            self.month_label.set_text("Project month: " + str(self.months))
            self.mpl.redraw(self.months)
            self.funds -= self.hire_cost*self.number_of_coders
            self.funds += self.assets*30
            self.funds_label.set_text("Available funds: £" + str(self.funds))

        if self.lines_of_code > 10000 and not self.shippable:
            self.shippable = True
            self.ship_button.style.update({"visibility":"visible"})
            
    def main(self):
        # passes the widget and its contents to the Start class
        return self.master_container


start(A_humble_startup, debug=False, address='0.0.0.0', port=0, multiple_instance=False)




