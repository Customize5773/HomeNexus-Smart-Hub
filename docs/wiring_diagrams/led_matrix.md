graph LR
    RPI[<b>RPi GPIO</b>] -->|BCM 5| LED1[LED 1]
    RPI -->|BCM 6| LED2[LED 2]
    RPI -->|BCM 13| LED3[LED 3]
    RPI -->|BCM 19| LED4[LED 4]
    RPI -->|BCM 26| LED5[LED 5]
    RPI -->|BCM 21| LED6[LED 6]
    
    LED1 --> R1[220Ω Resistor]
    LED2 --> R2[220Ω Resistor]
    LED3 --> R3[220Ω Resistor]
    LED4 --> R4[220Ω Resistor]
    LED5 --> R5[220Ω Resistor]
    LED6 --> R6[220Ω Resistor]
    
    R1 --> GND[Common Ground]
    R2 --> GND
    R3 --> GND
    R4 --> GND
    R5 --> GND
    R6 --> GND
    
    classDef led fill:#e6f7ff,stroke:#1890ff;
    class LED1,LED2,LED3,LED4,LED5,LED6 led;
