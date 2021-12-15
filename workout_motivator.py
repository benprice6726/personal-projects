import keyboard
import threading
from datetime import datetime
import tkinter as tk
import random as rand
import time


class Motivator:
    def __init__(self,work_set,end_time,clock_increment,interval):
        self.start_time=datetime.now()
        self.work_set=work_set#workouts to do, as list of strings
        self.end_time=end_time
        self.clock_increment=clock_increment#Lets you choose whether to compare hours, hours+minutes, or hours+minutes+seconds
        self.interval=interval
        self.rep_tracker={key:0 for key in self.work_set}
        print(self.start_time)
        print(self.rep_tracker)
        

    def pop_up(self):
        pop=tk.Tk()
        w=800
        h=400
        sw=pop.winfo_screenwidth()
        sh=pop.winfo_screenheight()
        x=(sw-w)/2
        y=(sh-h)/2
        pop.geometry('%dx%d+%d+%d' % (w,h,x,y))
        rand_num=rand.randrange(0,len(self.work_set))
        num_reps=rand.randint(10,20)
        self.rep_tracker[self.work_set[rand_num]]+=num_reps
        label=tk.Label(pop,text=self.work_set[rand_num]+"\n"+str(num_reps)+" reps",width=120,height=10)
        label.pack()
        close_button=tk.Button(pop,text="CLOSE",command=pop.destroy,width=10)
        close_button.pack() 
        pop.mainloop()

    def day_timer(self): 
        #input end_time in 24 hr time as hh:mm:ss
        self.EOD=False
        curr=datetime.now()
        str_curr=str(curr)
        if self.clock_increment=="h":
            curr_t1=str_curr.split(" ")
            curr_t2=curr_t1[1].split(":")
            self.current_time=curr_t2[0]
            self.modified_end_time=self.end_time.split(":")[0]
        elif self.clock_increment=="m":
            curr_t1=str_curr.split(" ")
            curr_t2=curr_t1[1].split(":")
            self.current_time=curr_t2[0]+":"+curr_t2[1]
            self.modified_end_time=self.end_time.split(":")[0]+":"+self.end_time.split(":")[1]
        elif self.clock_increment=="s":
            curr_t1=str_curr.split(" ")
            curr_t2=curr_t1[1].split(":")
            self.current_time=curr_t2[0]+":"+curr_t2[1]+":"+curr_t2[2].split(".")[0]
            self.modified_end_time=self.end_time
        print(self.current_time)
        print(self.modified_end_time)
        if self.current_time>=self.modified_end_time:
            self.EOD=True
            print("End of day reached")
        return(self.EOD)


    def callback(self,event):
        self.key_pressed=True

    def key_checker(self):
        while not self.day_timer():
            while not self.key_pressed:
                time.sleep(self.interval)
                if self.key_pressed:
                    break
                self.pop_up()
                print("getting swol")
            self.key_pressed=False


    def run(self):
        self.key_pressed=False
        self.EOD=False
        key_click_handle=keyboard.on_release(callback=self.callback)
        key_click_thrd=threading.Thread(target=key_click_handle,daemon=True)
        key_check_handle=self.key_checker()
        key_check_thrd=threading.Thread(target=key_check_handle,daemon=True)
        print("Started at "+str(self.start_time))
        print(self.rep_tracker)


blah=Motivator(["push ups","sit ups","squats"],"18:20:00","m",120)
blah.run()