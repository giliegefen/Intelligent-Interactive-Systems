import tkinter as tk
from tkinter import *
from tkinter import messagebox
#import tkMessageBox
import time
import random
import numpy as np
import copy
from copy import deepcopy


dist = random.random()
print(dist)

exp_dist=[0.464,0.207,0,0.268,0.07]
orig_dist=[0.2, 0.2, 0.2, 0.2, 0.2]
rand_dist=[0.25,0.10,0.11,0.28,0.26]
my_dist=[0.5,0,0,0,0.5]

class GUI:
    def __init__(self, min_button_size=30, total_space=500, button_distributions=my_dist, num_trials=20, adaptive=True):
        self.prev_time = int(round(time.time() * 1000))
        self.buttons = []  # the buttons in the GUI
        self.button_labels = ['A', 'B', 'C', 'D', 'E']  # labels for buttons
        self.button_distribution = button_distributions  # distribution of buttons to be clicked on
        self.counts = [0.0, 0.0, 0.0, 0.0, 0.0]  # number of times each button was clicked on
        self.times = []  # times between clicks
        self.min_button_size = min_button_size  # minimal button width
        self.total_space = total_space  # the total width that can be used by buttons
        self.button_text = self.button_labels[self.choose_next_button()]  # select which button should be clicked on next
        self.errors = 0.0  # error counter
        self.trials = 0.0  # trial counter
        self.num_trials = num_trials  # total number of trials in the experiment
        self.adaptive = adaptive  # whether button sizes should be adaptively modified or not
        #self.adaptive = False

        # generate the GUI
        self.root = tk.Tk()
        frame = tk.Frame(self.root)
        frame.pack()
        pixel = tk.PhotoImage(width=1, height=1)
        buttonA = tk.Button(frame,
                           text="A",
                           width=100, height=100,
                           command=lambda: self.log_click(0), image=pixel, compound="c")
        buttonA.pack(side=tk.LEFT)
        buttonB = tk.Button(frame,
                           text="B", width=100, height=100,
                           command=lambda: self.log_click(1), image=pixel, compound="c")
        buttonB.pack(side=tk.LEFT)
        buttonC = tk.Button(frame,
                           text="C", width=100, height=100,
                           command=lambda: self.log_click(2), image=pixel, compound="c")
        buttonC.pack(side=tk.LEFT)
        buttonD = tk.Button(frame,
                           text="D", width=100, height=100,
                           command=lambda: self.log_click(3), image=pixel, compound="c")
        buttonD.pack(side=tk.LEFT)
        buttonE = tk.Button(frame,
                           text="E", width=100, height=100,
                           command=lambda: self.log_click(4), image=pixel, compound="c")
        buttonE.pack(side=tk.LEFT)
        self.buttons.append(buttonA)
        self.buttons.append(buttonB)
        self.buttons.append(buttonC)
        self.buttons.append(buttonD)
        self.buttons.append(buttonE)
        self.T = Text(self.root, height=1, width=3,font=("Helvetica", 24))
        self.T.tag_configure("center", justify='center')
        self.T.insert("1.0", self.button_text)
        self.T.tag_add("center", "1.0", "end")
        self.T.pack()

        self.root.mainloop()  # run the GUI

    def choose_next_button(self):
        """
        Chooses which button should be clicked on next based on the button distribution
        :return: index of button that should be clicked on next
        """

        rand = random.random()
        sum_prob = 0.0
        i = -1
        while sum_prob < rand:
            i += 1
            sum_prob += self.button_distribution[i]

        return i

    def resize_buttons(self):
        """
        Modifies button width such that:
        -Each button width is at least of min_size_button (i.e., if the button was never clicked it should still have the
        minimal size as defined
        -The total space used is as defined by total_space
        -The space that remains after allocating the minimal space to buttons that have never been clicked should be
        divided between the buttons that were clicked such that the width of these buttons is proportional to the number
        of times they have been clicked on.
        -Example: if A and B were each clicked on once, and C,D,E have never been clicked on, then C,D,E should each have
        a width = 30 (as defined by min_button_size). This takes 90 pixels out of the 500 (as defined by total_space).
        The remaining 410 pixels should be equally divided between A and B (i.e., each of the will have width = 205)
        HINT: to modify button size, you can use: self.buttons[i].config(width=desired_width) (you need to compute the
        desired width)
        - IMPORTANT: if self.adaptive = false, you should NOT change button sizes
        :return: does not return anything; modifies the GUI
        """
        if self.adaptive == False: return

        desired_width = deepcopy(self.button_distribution)
        # quantify how many units to give per click per button (not including buttons that were not clicked on)
        num_zero=self.counts.count(0)
        nom=self.total_space-(num_zero*self.min_button_size)

        num_units=0
        for i in range(len(self.counts)):
            if self.counts[i]!= 0:
                num_units=num_units+self.counts[i]
        if num_units ==0:
            num_units =1
        unit= nom/num_units


        for i in range(len(self.counts)):
            check=self.counts[i]
            if check == 0:
                desired_width[i]= self.min_button_size
            else:
                desired_width[i]= (unit*check)

        for i in range(len(self.counts)):
            self.buttons[i].config(width=desired_width[i])

        # TODO: complete this function. It should adjust the button width based on its frequency of use

       # pass

    def log_click(self, i):
        """
        logs the button that was clicked on, the time it took the user to click it, if the user clicked the wrong button
        logs the error; presents the next button to click on
        :param i: the index of the button that was clicked on
        :return: nothing
        """
        self.trials += 1
        if self.button_labels[i] != self.button_text:  # log error if user clicked the wrong button
            self.errors += 1
        self.counts[i] += 1  # increment click count for button
        millis = int(round(time.time() * 1000))  # get current time
        self.times.append(millis-self.prev_time)  # log the time it took the user to click
        self.prev_time = millis
        self.resize_buttons()  # modify button size to reflect change in click counts
        if self.trials < self.num_trials:  # choose and present next button the user should click on
            self.button_text = self.button_labels[self.choose_next_button()]
            self.T.delete(1.0)
            self.T.insert("1.0", self.button_text)
            self.T.tag_add("center", "1.0", "end")
        else:  # experiment ended, outputs the average time between clicks and error rate
            print( 'end of trial!')
            print('mean click time = ' + str(np.mean(self.times)/1000.0))
            print('percent errors =' + str(self.errors/self.num_trials))
            messagebox._show('end of trial!', 'mean click time = '+ str(np.mean(self.times)/1000.0) +
                               '; percent errors =' + str(self.errors/self.num_trials))


if __name__ == '__main__':
    ui = GUI()



