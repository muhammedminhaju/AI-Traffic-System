#define R1_G 2
#define R1_Y 3
#define R1_R 4

#define R2_G 5
#define R2_Y 6
#define R2_R 7

#define R3_G 8
#define R3_Y 9
#define R3_R 10

void setup() {

  Serial.begin(9600);

  pinMode(R1_G, OUTPUT);
  pinMode(R1_Y, OUTPUT);
  pinMode(R1_R, OUTPUT);

  pinMode(R2_G, OUTPUT);
  pinMode(R2_Y, OUTPUT);
  pinMode(R2_R, OUTPUT);

  pinMode(R3_G, OUTPUT);
  pinMode(R3_Y, OUTPUT);
  pinMode(R3_R, OUTPUT);

  allOff();
}

void loop() {

  if (Serial.available()) {

    String data = Serial.readStringUntil('\n');

    if (data == "GRR") {

      digitalWrite(R1_G,LOW);
      digitalWrite(R1_Y,HIGH);
      digitalWrite(R1_R,HIGH);

      digitalWrite(R2_G,HIGH);
      digitalWrite(R2_Y,HIGH);
      digitalWrite(R2_R,LOW);

      digitalWrite(R3_G,HIGH);
      digitalWrite(R3_Y,HIGH);
      digitalWrite(R3_R,HIGH);
    }

    else if (data == "RRR") {

      digitalWrite(R1_G,HIGH);
      digitalWrite(R1_Y,HIGH);
      digitalWrite(R1_R,LOW);

      digitalWrite(R2_G,HIGH);  
      digitalWrite(R2_Y,HIGH);
      digitalWrite(R2_R,LOW);

      digitalWrite(R3_G,HIGH);
      digitalWrite(R3_Y,HIGH);
      digitalWrite(R3_R,HIGH);
    }

    else if (data == "YYY") {

      digitalWrite(R1_G,HIGH);
      digitalWrite(R1_Y,LOW);
      digitalWrite(R1_R,HIGH);

      digitalWrite(R2_G,HIGH);
      digitalWrite(R2_Y,LOW);
      digitalWrite(R2_R,HIGH);

      digitalWrite(R3_G,HIGH);
      digitalWrite(R3_Y,LOW);
      digitalWrite(R3_R,LOW);
    }

    else if (data == "GGG") {

      digitalWrite(R1_G,LOW);
      digitalWrite(R1_Y,HIGH);
      digitalWrite(R1_R,HIGH);

      digitalWrite(R2_G,LOW);
      digitalWrite(R2_Y,HIGH);
      digitalWrite(R2_R,HIGH);

      digitalWrite(R3_G,LOW);
      digitalWrite(R3_Y,HIGH);
      digitalWrite(R3_R,LOW);
    }

    else if (data == "RGR") {

      digitalWrite(R1_G,HIGH);
      digitalWrite(R1_Y,HIGH);
      digitalWrite(R1_R,LOW);

      digitalWrite(R2_G,LOW);
      digitalWrite(R2_Y,HIGH);
      digitalWrite(R2_R,HIGH);

      digitalWrite(R3_G,HIGH);
      digitalWrite(R3_Y,HIGH);
      digitalWrite(R3_R,HIGH);
    }

    else if (data == "RRG") {

      digitalWrite(R1_G,HIGH);
      digitalWrite(R1_Y,HIGH);
      digitalWrite(R1_R,LOW);

      digitalWrite(R2_G,HIGH);
      digitalWrite(R2_Y,HIGH);
      digitalWrite(R2_R,LOW);

      digitalWrite(R3_G,LOW);
      digitalWrite(R3_Y,HIGH);
      digitalWrite(R3_R,LOW);
    }
    else if(data == "YRR"){
       digitalWrite(R1_G,HIGH);
      digitalWrite(R1_Y,LOW);
      digitalWrite(R1_R,HIGH);

      digitalWrite(R2_G,HIGH);
      digitalWrite(R2_Y,HIGH);
      digitalWrite(R2_R,LOW);

      digitalWrite(R3_G,HIGH);
      digitalWrite(R3_Y,HIGH);
      digitalWrite(R3_R,HIGH);

    }

        else if(data == "RYR"){
       digitalWrite(R1_G,HIGH);
      digitalWrite(R1_Y,HIGH);
      digitalWrite(R1_R,LOW);

      digitalWrite(R2_G,HIGH);
      digitalWrite(R2_Y,LOW);
      digitalWrite(R2_R,HIGH);

      digitalWrite(R3_G,HIGH);
      digitalWrite(R3_Y,HIGH);
      digitalWrite(R3_R,HIGH);

    }
    else if(data == "RRY"){
       digitalWrite(R1_G,HIGH);
      digitalWrite(R1_Y,HIGH);
      digitalWrite(R1_R,LOW);

      digitalWrite(R2_G,HIGH);
      digitalWrite(R2_Y,HIGH);
      digitalWrite(R2_R,LOW);

      digitalWrite(R3_G,HIGH);
      digitalWrite(R3_Y,LOW);
      digitalWrite(R3_R,LOW);

    }
else if (data == "stop") {

      digitalWrite(R1_G,HIGH);
      digitalWrite(R1_Y,HIGH);
      digitalWrite(R1_R,HIGH);

      digitalWrite(R2_G,HIGH);
      digitalWrite(R2_Y,HIGH);
      digitalWrite(R2_R,HIGH);

      digitalWrite(R3_G,HIGH);
      digitalWrite(R3_Y,HIGH);
      digitalWrite(R3_R,LOW);
    }

  }
}

void allOff(){

  digitalWrite(R1_G, HIGH);
  digitalWrite(R1_Y, HIGH);
  digitalWrite(R1_R, HIGH);

  digitalWrite(R2_G, HIGH);
  digitalWrite(R2_Y, HIGH);
  digitalWrite(R2_R, HIGH);

  digitalWrite(R3_G, HIGH);
  digitalWrite(R3_Y, HIGH);
  digitalWrite(R3_R, LOW);   // OFF for Active HIGH relay

}