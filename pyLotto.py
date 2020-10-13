#!/usr/bin/python3
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import os                       # for file handling
from datetime import datetime   # for loading/saving bets
from datetime import timedelta  # for today - 1
import csv

betsFile    =   './MyBets.csv'
oldwinners  =   './MyData.csv'
tmpfile     =   './newData.tmp'
newnumbers    = [0,0,0,0,0,0,0]
number = 0

class pyLotto:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("PyLotto.glade")
        self.builder.connect_signals(self)
        self.builder.get_objects()
        self.model = self.builder.get_object('bets')
        self.list = self.builder.get_object('lstBets')
        
        column = Gtk.TreeViewColumn('First', Gtk.CellRendererText(), text=0)   
        self.list.append_column(column)
        column = Gtk.TreeViewColumn('Second', Gtk.CellRendererText(), text=1)   
        self.list.append_column(column)
        column = Gtk.TreeViewColumn('Third', Gtk.CellRendererText(), text=2)   
        self.list.append_column(column)
        column = Gtk.TreeViewColumn('Fourth', Gtk.CellRendererText(), text=3)   
        self.list.append_column(column)
        column = Gtk.TreeViewColumn('Fifth', Gtk.CellRendererText(), text=4)   
        self.list.append_column(column)
        column = Gtk.TreeViewColumn('Sixth', Gtk.CellRendererText(), text=5)   
        self.list.append_column(column)
        
        self.loadBets()
                
    def onDestroy(self, *args):
        Gtk.main_quit()

    def launch(self):
        window = self.builder.get_object("MainWindow")
        window.show_all()
        Gtk.main()
    
    def exit_app(self, btnExit):
        Gtk.main_quit()
    
    def checkLastTen(self, btnCheckLast10):
        x = 0
        winners = 0
        self.showmessage("Checking last 10")
        with open(oldwinners) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for csvrow in csv_reader:
                if x == 10:
                    break
                x += 1
                for row in range(0, 11):
                    matches = bonusmatch = 0
                    self.model = self.builder.get_object('bets')
                    betlist = self.model[row][:]
                    print(str(csvrow) + "\n" + str(betlist))
                    for j in range(1, len(csvrow)):
                        for n in range(0, len(betlist)):
                            if int(betlist[n]) == int(csvrow[j]):
                                if n < len(betlist) - 1:
                                    matches += 1
                                else:
                                    bonusmatch +=1
                    if matches >= 5:
                        message = "HUGE! Matches = " + str(matches) + "bonus match = " + str(bonusmatch) + "\n" + str(csvrow)
                        winners += 1
                        self.showmessage(message)
                    elif matches == 4:
                        message = "Winner Matches = " + str(matches + "\n" + str(csvrow))
                        winners += 1
                        self.showmessage(message)
                    elif matches == 3:
                        message = "Maybe I got you a dollar?" + "\n" + str(csvrow)
                        winners += 1
                        self.showmessage(message)
            if winners == 0:
                message = "Better luck next time fella."
                self.showmessage(message)
                
    def compareBets(self):
        winners = 0
        for row in range(0, 11):
            self.model = self.builder.get_object('bets')
            betlist = self.model[row][:]
            print(betlist)
            matches = bonusmatch = 0

            for n in range(0, len(newnumbers)):
                for x in range(0, len(betlist)):
                    if int(newnumbers[n]) == int(betlist[x]):
                        if n < len(newnumbers)-1:
                            matches +=1
                        else:
                            bonusmatch +=1
            if matches >= 5:
                message = "HUGE! Matches = " + str(matches) + "bonus match = " + str(bonusmatch) + "\n" + str(betlist)
                winners += 1
                self.showmessage(message)
            elif matches == 4:
                message = "Winner Matches = " + str(matches + "\n" + str(betlist))
                winners += 1
                self.showmessage(message)
            elif matches == 3:
                message = "Maybe I got you a dollar?" + "\n" + str(betlist)
                winners += 1
                self.showmessage(message)
        if winners == 0:
            message = "Better luck next time fella."
            self.showmessage(message)

    def showmessage(self, message):
        dialog = Gtk.MessageDialog(
            self.builder.get_object("MainWindow"),
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()

    def save_latest(self, btnSaveLatest):
        self.getlatest()
        today = datetime.today()
        today -= timedelta(days=1)
        todaylist = [today.strftime('%m/%d/%y'),newnumbers[0],newnumbers[1],newnumbers[2],newnumbers[3],newnumbers[4],newnumbers[5],newnumbers[6],]
        with open(tmpfile, mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(todaylist)
            with open(oldwinners) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    writer.writerow(row)
        os.remove(oldwinners)
        os.rename(tmpfile, oldwinners)
        self.showmessage("Newest numbers saved.")

    def check_new(self, btnCheckNew):
        self.getlatest()
        print(newnumbers)
        # Now, load mybets into lstBets and compare to mybets for winner
        self.compareBets()

    def loadBets(self):
        ifile = open(betsFile, 'r')
        reader = csv.reader(ifile)
        for row in reader:
            self.model.append(row)
    
    def getlatest(self):
        entry     = self.builder.get_object("num1")
        if entry.get_text() == "":
            print('must enter a number in each box')
            return
        newnumbers[0] = int(entry.get_text())
        entry     = self.builder.get_object("num2")
        if entry.get_text() == "":
            print('must enter a number in each box')
            return
        newnumbers[1] = int(entry.get_text())
        entry     = self.builder.get_object("num3")
        if entry.get_text() == "":
            print('must enter a number in each box')
            return
        newnumbers[2] = int(entry.get_text())
        entry     = self.builder.get_object("num4")
        if entry.get_text() == "":
            print('must enter a number in each box')
            return
        newnumbers[3] = int(entry.get_text())
        entry     = self.builder.get_object("num5")
        if entry.get_text() == "":
            print('must enter a number in each box')
            return
        newnumbers[4] = int(entry.get_text())
        entry     = self.builder.get_object("num6")
        if entry.get_text() == "":
            print('must enter a number in each box')
            return
        newnumbers[5] = int(entry.get_text())
        entry     = self.builder.get_object("num7")
        if entry.get_text() == "":
            print('must enter a number in each box')
            return
        newnumbers[6] = int(entry.get_text())
            
        
        
# Run pyLotto:
myapp = pyLotto()
myapp.launch()
