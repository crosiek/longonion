import serial, time

class styr_printer(object):
  ser = None
  
  def wait_for(self, s):
    line = ''
    while line != s:
      line = self.ser.readline()
      print(line)

  def start(self):
    # Wait for the printer to be ready to receive
    self.wait_for(b'echo:busy: processing\n')
    time.sleep(1)
    
    # Set absolute positioning
    self.ser.write(b'G90\n')
    self.wait_for(b'ok\n')
    
    print('Printer is now ready!')
    
  def home(self):
    # Send the home command and wait for results
    self.ser.write(b'G28 \n')
    self.wait_for(b'ok\n')
    time.sleep(1)
    
    print('Printer is now homed')
    
  def move(self, direction, amount):
    self.ser.write('G1 {}{} \n'.format(direction, amount).encode('utf-8'))
    self.wait_for(b'ok\n')
    self.ser.write(b'G4 P1 \n')
    self.wait_for(b'ok\n')
    time.sleep(0.1)
    
  def move_x(self, amount):
    self.move('X', amount)
    
  def move_y(self, amount):
    self.move('Y', amount)
    
  def move_z(self, amount):
    self.move('Z', amount)
    
  def main(self):
    with serial.Serial('/dev/cu.usbmodem1411', 115200, timeout = 2) as ser:
      self.ser = ser
      
      self.start()
      self.home()
      
      self.move_z(12.3)
      self.move_x(121.1)
      #self.move_y(12.2)
      

if __name__ == '__main__':
  s = styr_printer()
  s.main()
