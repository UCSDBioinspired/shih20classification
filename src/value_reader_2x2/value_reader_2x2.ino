/* Skin Robot Value Reader to serial out
 * 
 * B. Shih, E. Lathrop, I. Adibnazari, R. Martin, Y. L. Park, M. T. Tolley, “Classification of components ofaffective touch using rapidly manufacturable, soft, sensor skins”, 2019, submitted.
 * 
 */


// Dynamic thresholding for calibration. initial values don't matter.
int THRESHOLD0 = 147;
int THRESHOLD1 = 85;
int THRESHOLD2 = 287;
int THRESHOLD3 = 120;

int OFFSET = -2; // how much buffer room to give the threshold value [units: 8 bit analog, 0 to 255]
int calibWindow = 10; // number of samples to average over
boolean initialized = false; // flag for the calibration process.


// Initialize float force sensor values
float FS0, FS1, FS2, FS3;  


// Initialize above variables as Input sensors in accordance to pin
void setup() {

  // initialize input pins A1-A4 on Arduino, if more sensors add to section
  pinMode(A0, INPUT); 
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT); 

  Serial.begin(115200); // begin max data collection (max bit count)

}


// When calling this function, ensure that nothing is in contact with the sensor.
void calibrate()
{
  // average the last [calibWindow] values
  int calib0[calibWindow];
  int calib1[calibWindow];
  int calib2[calibWindow];
  int calib3[calibWindow];

  for (int i = 0; i < calibWindow; i++)
  {
    calib0[i] = analogRead(A0);
    calib1[i] = analogRead(A1);
    calib2[i] = analogRead(A2);
    calib3[i] = analogRead(A3);
    delay(100);
  }

  THRESHOLD0 = avgArray(calib0) - OFFSET;
  THRESHOLD1 = avgArray(calib1) - OFFSET;
  THRESHOLD2 = avgArray(calib2) - OFFSET;
  THRESHOLD3 = avgArray(calib3) - OFFSET;

}


int avgArray(int threshArray[]){
  int sum = 0;
  for (int j = 0; j < calibWindow; j++)
  {
      sum += threshArray[j];
  }
  return sum / calibWindow;
}


// Main Loop: Read inputs, Output Values
void loop() 
{
  // Calibration process
  if (false == initialized)
  {
    calibrate();
    //Serial.println("Calibrating threshold values");
    initialized = true;
  }

  // Data acquisition
  FS0 = analogRead(A0); // read force sensor 0
  FS1 = analogRead(A1); // read force sensor 1
  FS2 = analogRead(A2); // read force sensor 2
  FS3 = analogRead(A3); // read force sensor 3

// simple if statements to read if any sensors are touched, avoid noise > 50

/*
//1x1
if (FS0 > THRESHOLD0){
  Serial.println((float)FS0 - THRESHOLD0);
  delay(5);
}
*/

  
//3x3
if (FS0 > (THRESHOLD0 + 5) || FS1 > (THRESHOLD1 + 5) || FS2 > (THRESHOLD2 + 5) || FS3 > (THRESHOLD3 + 5))
{
  Serial.print((float)FS0 - THRESHOLD0 );
  Serial.print(",");
  Serial.print((float)FS1 - THRESHOLD1 );
  Serial.print(",");
  Serial.print((float)FS2 - THRESHOLD2 );
  Serial.print(",");
  Serial.print((float)FS3 - THRESHOLD3 );
  Serial.println("");
  delay(5);
}


}
