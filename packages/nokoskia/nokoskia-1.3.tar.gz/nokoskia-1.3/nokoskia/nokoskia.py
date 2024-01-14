import curses 
from curses import wrapper
import time

def knock():
    def main(stdscr):

        # Check if the terminal supports colors
        curses.start_color()
        # Define color pairs (foreground, background)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

        curses.curs_set(0)
        
        stdscr.clear();
        stdscr.refresh();
        
        # adding the co-ordinates to be the top-left corner as default.
        x = 0;
        y = 0;
        
        # splitting the dialogue into two variables making it easy to change the color of the sentences in the sameline.
        part1 = "I am the One Who ";
        part2 = "KNOCKS."

        try:
            # making the loop always true to give it a infinite behaviour.
            while True:
                # getting the size of the terminal window, to avoid error like "characters out of the visible area error"
                height, width = stdscr.getmaxyx();
                # checking whether the line is within the visible area.
                if x < height:
                    stdscr.addstr(x, y, part1, curses.color_pair(1))
                    stdscr.addstr(x, y + len(part1), part2, curses.color_pair(2) | curses.A_BOLD)
                    x = x+1;
                    stdscr.refresh();
                    # if the line is going to outside the visible area, then:
                else:
                    # erase the screen and start from the beginning.
                    stdscr.erase();
                    x = 0
                time.sleep(0.1);
        except KeyboardInterrupt:
            pass

    wrapper(main);

