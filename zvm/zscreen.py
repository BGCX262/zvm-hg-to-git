#
# A template class representing the screen of a z-machine.
#
# Third-party programs are expected to subclass zscreen and override all
# the methods, then pass an instance of their class to be driven by
# the main z-machine engine.
#
# For the license of this file, please consult the LICENSE file in the
# root directory of this distribution.
#

import zstream

# Constants for window numbers.
#
# TODO: The Z-Machine standard mentions upper and lower windows and
# window numbers, but never appears to define a mapping between the
# two.  So the following values are simply a best guess and may need
# to be changed in the future.
WINDOW_UPPER = 1
WINDOW_LOWER = 2

# Constants for fonts.  These are human-readable names for the font ID
# numbers as described in section 8.1.2 of the Z-Machine Standards
# Document.
FONT_NORMAL = 1
FONT_PICTURE = 2
FONT_CHARACTER_GRAPHICS = 3
FONT_FIXED_PITCH = 4


class ZScreenObserver(object):
  """Observer that is notified of changes in the state of a ZScreen
  object.

  Note that all methods in this class may be called by any thread at
  any time, so they should take any necessary precautions to ensure
  the integrity of any data they modify."""

  def on_screen_size_change(self, zscreen):
    """Called when the screen size of a ZScreen changes."""

    pass

  def on_font_size_change(self, zscreen):
    """Called when the font size of a ZScreen changes."""

    pass


class ZScreen(zstream.ZBufferableOutputStream):
  """Subclass of zstream.ZBufferableOutputStream that provides an
  abstraction of a computer screen."""

  def __init__(self):
    "Constructor for the screen."

    # The size of the screen.
    self._columns = 80
    self._rows = 24

    # The size of the current font, in characters
    self._fontheight = 1
    self._fontwidth = 1

    # List of our observers; clients can directly append to and remove
    # from this.
    self.observers = []

    # Subclasses must define real values for all the features they
    # support (or don't support).

    self.features = {
      "has_status_line" : False,
      "has_upper_window" : False,
      "has_graphics_font" : False,
      "has_text_colors":  False,
      }

  # Window Management
  #
  # The z-machine has 2 windows for displaying text, "upper" and
  # "lower".  (The upper window has an inital height of 0.)
  #
  # The upper window is not necessarily where the "status line"
  # appears; see section 8.6.1.1 of the Z-Machine Standards Document.
  #
  # The UI is responsible for making the lower window scroll properly,
  # as well as wrapping words ("buffering").  The upper window,
  # however, should *never* scroll or wrap words.
  #
  # The UI is also responsible for displaying [MORE] prompts when
  # printing more text than the screen-height can display.  (Note: if
  # the screen height is 255, then it should never prompt [MORE].)

  def get_screen_size(self):
    """Return the current size of the screen as [rows, columns]."""

    return [self._rows, self._columns]
  
  def select_window(self, window):
    """Select a window to be the 'active' window, and move that
    window's cursor to the upper left.

    WINDOW should be one of WINDOW_UPPER or WINDOW_LOWER.

    This method should only be implemented if the
    has_upper_window feature is enabled."""

    raise NotImplementedError()


  def split_window(self, height):
    """Make the upper window appear and be HEIGHT lines tall.  To
    'unsplit' a window, call with a height of 0 lines.

    This method should only be implemented if the has_upper_window
    feature is enabled."""

    raise NotImplementedError()


  def set_cursor_position(self, x, y):
    """Set the cursor to (row, column) coordinates (X,Y) in the
    current window, where (1,1) is the upper-left corner.

    This function only does something if the current window is the
    upper window; if the current window is the lower window, this
    function has no effect.
    
    This method should only be implemented if the
    has_upper_window feature is enabled."""

    raise NotImplementedError()


  def erase_window(self, window, color):
    """Erase WINDOW to background COLOR.

    WINDOW should be one of WINDOW_UPPER or WINDOW_LOWER.

    If the has_upper_window feature is not supported, WINDOW is
    ignored (in such a case, this function should clear the entire
    screen).

    If the has_text_colors feature is not supported, COLOR is ignored."""

    raise NotImplementedError()


  def erase_line(self):
    """Erase from the current cursor position to the end of its line
    in the current window.  If the has_upper_window feature is
    unsupported, this function applies to the entire screen."""

    raise NotImplementedError()


  # Status Line
  #
  # These routines are only called if the has_status_line capability
  # is set.  Specifically, one of them is called whenever the
  # show_status opcode is executed, and just before input is read from
  # the user.

  def print_status_score_turns(self, text, score, turns):
    """Print a status line in the upper window, as follows:

        On the left side of the status line, print TEXT.
        On the right side of the status line, print SCORE/TURNS.

    This method should only be implemented if the has_status_line
    feature is enabled.
    """

    raise NotImplementedError()


  def print_status_time(self, hours, minutes):
    """Print a status line in the upper window, as follows:

        On the left side of the status line, print TEXT.
        On the right side of the status line, print HOURS:MINUTES.

    This method should only be implemented if the has_status_line
    feature is enabled.
    """

    raise NotImplementedError()


  # Text Appearances
  #

  def get_font_size(self):
    """Return the current font's size as [width, height]."""

    return [self._fontwidth, self._fontheight]


  def set_font(self, font_number):
    """Set the current window's font to one of

          FONT_NORMAL - normal font
          FONT_PICTURE - picture font (IGNORE, this means nothing)
          FONT_CHARACTER_GRAPHICS - character graphics font
          FONT_FIXED_WIDTH - fixed-width font

    If a font is not available, return None.  Otherwise, set the
    new font, and return the number of the *previous* font."""

    raise NotImplementedError()


  def set_text_style(self, style_number):
    """Set the current text style to one of

           0 - Roman
           1 - Reverse video
           2 - Bold
           4 - Italic
           8 - Fixed-width"""

    raise NotImplementedError()


  def set_text_color(self, foreground_color, background_color):
    """Set current text foreground and background color to values in

            0 - current color
            1 - default color
            2 - black,  3 - red, 4 - green, 5 -yellow, 6 - blue,
            7 - magenta, 8 - cyan, 9 - white, 10 - dark grey,
            11- medium grey, 12 - dark grey

    This method should only be implemented if the has_text_colors
    feature is enabled.
    """

    raise NotImplementedError()


  # Standard output

  def write(self, string):
    """Implementation of the ZOutputStream method.  Prints the given
    unicode string to the currently active window, using the current
    text style settings."""

    raise NotImplementedError()
