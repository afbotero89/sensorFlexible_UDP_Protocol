<?
include('index_AdviceRealTime.html');
?>
<html>
<br>
<style type="text/css">

</style>
<title>Distribución de Presión</title>

<center>
<body>
<script src="https://js.pusher.com/3.1/pusher.min.js"></script>

<div>
    <!-- Div imagen paciente-->
    <div style="display: inline-block;">
        <img id="patient" src="./img/pacienteDeFrente2.png" style="WIDTH:230px; HEIGHT:400px"/>
    </div><!-- Div grafico presion--><div  style="display: inline-block;">
        <img id="pressurePlots" src="./img/GraficoPresion.jpg" style="WIDTH:1150px; HEIGHT:400px"/>
    </div>
    <div><!-- Div label inclinación de camilla y gráfico paciente inclinacion -->
      <div  style="display: inline-block;">
        
            <label  id="angle_Label"><p style="color:white;font-family:helvetica;font-size: 25px; WIDTH:230px; HEIGHT:100px; text-align: center;background-color: black;">Inclinaci&oacute;n camilla: 0&#176;</p></label>
            <img id="angle_Image" style = "WIDTH:100px; HEIGHT:100px;background-color: black;" src="./img/BedMonitorV2/BedMonitoreoV2.00045.png" align="center"/>
            <label  id="breathing_frequency"><p style="color:white;font-family:helvetica;font-size: 22px;WIDTH:230px; HEIGHT:100px;text-align: center;background-color: black;">Frecuencia respiratoria: <br>18 rpm</p></label>
          </div>

          <!-- Div grafico presion sobre el paciente -->
          <div style="display: inline-block;">
            <img id="pressureDistributionImagePatient" src="./img/historial1.png" style="WIDTH:1150px; HEIGHT:100px"/>
          <div>
          <center>
              <!-- Div imagen control de UCI -->
              <div  style="display: inline-block;">
                  <img id="control1" src="./img/control3.png" style="WIDTH:401px; HEIGHT:400px"/>
              </div>
                            <!-- Div imagen control de UCI -->
              <div  style="display: inline-block;">
                  <img id="control2" src="./img/control4.png" style="WIDTH:401px; HEIGHT:400px"/>
              </div>
          </center>
      </div>
</div>
</center>

</body> 
<script class="tablaHorario" language= "javascript" type= "text/javascript">

// Timers
setInterval(realtimeGraph_averagePressure, 1000);

setInterval(realtimeGraph_patient, 4000);

var patientCounter = 0

var control1 = 0;

var control2 = 0;

// Change real time plot
function realtimeGraph_averagePressure(){
    // Carga imagen sensor 1
    var imageName = "img/GraficoPresion.jpg?t=" + new Date().getTime();

    var imgSensor1 = new Image();
    imgSensor1.src = imageName;

    imgSensor1.onload = function(){ // Loaded successfully
      document.getElementById('pressurePlots').src = imgSensor1.src;
    };

    imgSensor1.onerror = function(){ // Failed to load
      console.log("failed to load");
    };
}

// Change real time patient
function realtimeGraph_patient(){
    // Carga imagen sensor 1

    patientCounter = patientCounter + 1;

    if (patientCounter == 8){
      patientCounter = 1;
    }

    var imageName = "img/historial" + patientCounter + ".png?t=" + new Date().getTime();

    var imgSensor1 = new Image();
    imgSensor1.src = imageName;

    imgSensor1.onload = function(){ // Loaded successfully
      document.getElementById('pressureDistributionImagePatient').src = imgSensor1.src;
    };

    imgSensor1.onerror = function(){ // Failed to load
      console.log("failed to load");
    };
}

// Change real advice control
function advice_control(){
    // Carga imagen sensor 1

    control1 = control1 + 1;

    if (control1 == 8){
      control1 = 1;
    }

    var imageName = "img/historial" + patientCounter + ".png?t=" + new Date().getTime();

    var imgSensor1 = new Image();
    imgSensor1.src = imageName;

    imgSensor1.onload = function(){ // Loaded successfully
      document.getElementById('pressureDistributionImagePatient').src = imgSensor1.src;
    };

    imgSensor1.onerror = function(){ // Failed to load
      console.log("failed to load");
    };
}

</script>
                    
</html>

