<?
include('index.html');
?>
<html>
<br>
<style type="text/css">

</style>
<title>Distribución de Presión</title>
<center> 
<body>
<script src="https://js.pusher.com/3.1/pusher.min.js"></script>

<div style = "position: absolute; right: 40px;">
<table width="100%" border="0" cellpadding="2">
    <tr>
        <td align="right">
           <img id="sensor1" src="" />
        </td>
        <td align="right">
           <img id="sensor2" src="" />
        </td>
        <td align="left">
           <img id="barraDePresion" src="./img/nivelDePresion.png" />
        </td>
    </tr>
</table>

</div>

<div style = "position: absolute; right: 10px;">
  <label  id="angle_Label" align="center"><p style="color:white;font-family:helvetica;font-size: 25px">Inclinaci&oacute;n:<br> 0&#176;   </p></label>
  <img id="angle_Image" WIDTH='100' HEIGHT='70' src="./img/Cama 400X400/Cama 400X400.00002.png" align="center"/>
</div>


<script class="tablaHorario" language= "javascript" type= "text/javascript">

      var myVar = setInterval(loadImages, 100);

      var estadoDeConexion = setInterval(revisaEstadoDeConexion, 1000);

      var tiemposSensor2 = document.getElementById('tiemposSensor2');

      var imagen = document.getElementById('img');

      var count = 0;

      var loadFailureState = false;

      var sensorConectado = false;

      var visualizaTiempos = false;


      function loadImages(){

          // Carga imagen sensor 1
          var imageName = "img/sensor1SinTiempos.jpeg?t=" + new Date().getTime();

          //var imageName1 = "img/imagen1.jpeg?t=" + new Date().getTime();
          var imageName1 = "img/sensor2SinTiempos.jpeg?t=" + new Date().getTime();

          if (visualizaTiempos == true){
            //imageName = "img/sensorCompleto.jpg?t=" + new Date().getTime();

            imageName = "img/sensor1.jpeg?t=" + new Date().getTime();
            imageName1 = "img/sensor2.jpeg?t=" + new Date().getTime();
            //imageNameSensor2 = "img/sensorComepleto.jpg?t=" + new Date().getTime();
          }
          
          var imgSensor1 = new Image();
          imgSensor1.src = imageName;

          var imgSensor2 = new Image();
          imgSensor2.src = imageName1;

          imgSensor1.onload = function(){ // Loaded successfully
              document.getElementById('sensor1').src = imgSensor1.src;
          };

          //**** Sensor 1 ****
          imgSensor1.onerror = function(){ // Failed to load
              console.log("failed to load");
          };


          imgSensor2.onload = function(){ // Loaded successfully
            
            document.getElementById('sensor2').src = imgSensor2.src;
            
          };

          //**** Sensor 1 ****
          imgSensor2.onerror = function(){ // Failed to load
              console.log("failed to load");
          };

          var deleteClient = function(id) {
            $.ajax({
            url: 'bridgePHP-Python.php',
            type: 'POST',
            data: {id:id},
            success: function(data) {

                var array = data.split(";")
                console.log(array[1]);
                if (parseInt(array[1])>=0 && parseInt(array[1])<50){
                  if (parseInt(array[1]) < 10){
                    if (parseInt(array[1])<7){
                      document.getElementById('angle_Image').src = "./img/Cama 400X400/Cama 400X400.0000" + "0" + ".png";
                    }else{
                      document.getElementById('angle_Image').src = "./img/Cama 400X400/Cama 400X400.0000" + array[1] + ".png";
                    }
 
                  }else{
                    document.getElementById('angle_Image').src = "./img/Cama 400X400/Cama 400X400.000" + array[1] + ".png";
                  }
                  if (parseInt(array[1])<7){
                      document.getElementById('angle_Label').innerHTML = "Inclinaci&oacute;n:<br>" + "0" + "&#176;";
                  }else{
                      document.getElementById('angle_Label').innerHTML = "Inclinaci&oacute;n:<br>" + array[1] + "&#176;";
                  }
                  document.getElementById('angle_Label').style.color = "white";
                  document.getElementById('angle_Label').style.fontSize = "20px";
                }
              }
            });
          };
          deleteClient("data");
      }

      function revisaEstadoDeConexion(){
        
        if(sensorConectado == false){
          sensorConectado = true
          document.getElementById('imageConnection').src = "./img/wifiDisconnected.png"
        }else{
          sensorConectado = false
          document.getElementById('imageConnection').src = "./img/wifiDisconnected.png"
        }
        
      }

      $(document).ready(function(){
        
        $('.expositionTimes').click(function(){
          if(visualizaTiempos == false){
            visualizaTiempos = true;
          }else{
            visualizaTiempos = false;
          }
          return false;
        });
      });

      $(document).ready(function(){
        
        $('.connectionState').click(function(){
          
          return false;
        });
      });

</script>

</script> 
</body> 
</center>                       
</html>

