
int LMF=11,RMF=7,LMB=12,RMB=5;
void setup() {
  // put your setup code here, to run once:
  pinMode(LMF,OUTPUT);
  pinMode(RMF,OUTPUT);
  pinMode(RMB,OUTPUT);
  pinMode(LMB,OUTPUT);
  Serial.begin(9600); 
}
void goForward()
  { digitalWrite(LMF,HIGH);
    digitalWrite(RMF,HIGH);
    digitalWrite(LMB,LOW);
    digitalWrite(RMB,LOW);
  }  
void Right()
  { digitalWrite(LMF,HIGH);
    digitalWrite(RMF,LOW);
    digitalWrite(LMB,LOW);
    digitalWrite(RMB,HIGH);
    delay(1000);
  }
void Left()
  {digitalWrite(LMF,LOW);
   digitalWrite(RMF,HIGH);
   digitalWrite(LMB,HIGH);
   digitalWrite(RMB,LOW);
    delay(1000);
  }  
void loop() {int i;
  // put your main code here, to run repeatedly:
    if(Serial.available()>0)
    {if(Serial.read()=='l')
        {Left();}
      else if(Serial.read()=='f')
        {goForward();} 
       else if(Serial.read()=='r')
        {Right();}
    }     
}
