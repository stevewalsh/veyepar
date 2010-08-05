#!/usr/bin/python

"""
tsdv.py - timestamp dv
sets start/end times of dv files

Gets start from one of:
the file system time stamp, 
the first frame of the dv
the file name (assumes hh:mm:ss.dv format)

duration (in seconds) based on file size / BBF*FPS 
last frame

"""

import  os
import datetime
# from dateutil.parser import parse

from process import process

from main.models import Client, Show, Location, Episode, Raw_File, Cut_List

class add_dv(process):

    def one_dv(self, dir, dv ):
        
        pathname = os.path.join(dir,dv.filename)
        print pathname
        filename = dv.filename

        # time-n gets used to avoid name colisions. 
        # for start/end, dupe time is fine, so drop the -n for parsing 
        if filename[-5]=='-': filename = filename[:-5] + filename[-3:] 
  
        # find a dir that looks like a date: 
        # shoud use os.split, but it is weird
        # for d in filename.split('/'):
        # make this work when really needed.
          
        # for now, the last dir is the date, and the file is time:
        filename='/'.join(filename.split('/')[-2:])

        start=datetime.datetime.strptime(filename,'%Y-%m-%d/%H:%M:%S.dv')
        # dt = dv.filename[:-3]
        # dt.replace('/',' ')
        st = os.stat(pathname)    
        # get start from filesystem create timestamp
        # start=datetime.datetime.fromtimestamp( st.st_mtime )
        # start=parse(dt)

        # use this to adjust for clock in wrong timezone
        start += datetime.timedelta(hours=self.options.offset_hours,minutes=0)
        if start.day in [17,18] and  dv.location.slug=='HanoverD':
                print dv.location.slug
                start += datetime.timedelta(hours=1,minutes=0)

        frames = st.st_size/self.bpf
        seconds = frames/self.fps 
        duration = seconds

        hours = int(duration / 3600)
        minutes = int((duration - hours*60)/60)
        seconds = duration - (hours*60 + minutes*60)
        duration = "%02d:%02d:%02d" % (hours, minutes,seconds)

        dv.start = start
        dv.duration = duration

        if not self.options.test:
            dv.save()


    def one_loc(self,show, location,dir):
      for dv in Raw_File.objects.filter(show=show, location=location):
        self.one_dv(dir,dv)

    def one_show(self, show):
      self.set_dirs(show)
      for loc in Location.objects.filter(show=show):
        dir=os.path.join(self.show_dir,'dv',loc.slug)
        print show,loc,dir
        self.one_loc(show, loc, dir)

    def work(self):
        """
        find and process show
        """
        if self.options.client and self.options.show:
            client = Client.objects.get(slug=self.options.client)
            show = Show.objects.get(client=client, slug=self.options.show)
            self.one_show(show)

        return

    def add_more_options(self, parser):
        parser.add_option('--offset_hours', type="int",
           help="adjust time to deal with clock in wrong time zone.")

    def add_more_option_defaults(self, parser):
        parser.set_defaults(offset_hours=0)


if __name__=='__main__': 
    p=add_dv()
    p.main()

