<?
include('index_UserSelectedUCIBed.html');
?>
<html>
<br>
<style type="text/css">

</style>
<title>Distribución de Presión</title>

<body>

<br>

<hr>

<script src="https://js.pusher.com/3.1/pusher.min.js"></script>

	<form action="UCIBedSelected.php">

		<center>

			<div>

				<div>

					<button type="submit" class="button" style="background: url(./img/pacienteUCI1.png); background-size:cover; border-radius: 25px;"></button>

					<button type="submit" class="button" style="background: url(./img/pacienteUCI1.png); background-size:cover; border-radius: 25px;"></button>

					<button type="submit" class="button" style="background: url(./img/pacienteUCI2.png); background-size:cover; border-radius: 25px;"></button>

					<button type="submit" class="button" style="background: url(./img/pacienteUCI2.png); background-size:cover; border-radius: 25px;"></button>

				</div>

				<div>

				  <button id = "UCIBed1" type="submit" style="width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url(./img/timer/TimerV2.00000.png);background-size:100px 100px;background-repeat: no-repeat;">00:00:00</button>

				  <button id = "UCIBed2" type="submit" style="width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url(./img/timer/TimerV2.00032.png);background-size:100px 100px;background-repeat: no-repeat;">00:00:01</button>

				  <button id = "UCIBed3" type="submit" style="width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url(./img/timer/TimerV2.00010.png);background-size:100px 100px;background-repeat: no-repeat;">00:00:02</button>

				  <button id = "UCIBed4" type="submit" style="width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url(./img/timer/TimerV2.00095.png);background-size:100px 100px;background-repeat: no-repeat;">00:00:03</button>
				  
				</div>

			</div>

		</center>

	</form>

</script>

<hr>

</body> 

</form>

<script class="tablaHorario" language= "javascript" type= "text/javascript">

	// Timers
	setInterval(setProperties_UCIBed1, 1000);

	setInterval(setProperties_UCIBed2, 1000);

	setInterval(setProperties_UCIBed3, 1000);

	setInterval(setProperties_UCIBed4, 1000);

	// Conuter images
	var imageNumberButton1 = 0;

	var imageNumberButton2 = 10;

	var imageNumberButton3 = 20;

	var imageNumberButton4 = 30;

	// Style buttons
	var styleButton1 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url(./img/timer/TimerV2.000" + 0 + 0 + ".png);background-size:100px 100px;background-repeat: no-repeat;";

	var styleButton2 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url(./img/timer/TimerV2.000" + 0 + 10 + ".png);background-size:100px 100px;background-repeat: no-repeat;";

	var styleButton3 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url(./img/timer/TimerV2.000" + 0 + 20 + ".png);background-size:100px 100px;background-repeat: no-repeat;";

	var styleButton4 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url(./img/timer/TimerV2.000" + 0 + 30 + ".png);background-size:100px 100px;background-repeat: no-repeat;";

	// Button timer 1
	function setProperties_UCIBed1(){

		  imageNumberButton1 = imageNumberButton1 + 1;

		  // Carga imagen sensor 1

	      if (imageNumberButton1 < 10){
	      	 var url = "./img/timer/TimerV2.000" + 0 + imageNumberButton1 + ".png?t=" + new Date().getTime();

			 styleButton1 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url(" + url +");background-size:100px 100px;background-repeat: no-repeat;";

	      }else{
	      	 var url = "./img/timer/TimerV2.000" + imageNumberButton1 + ".png?t=" + new Date().getTime();

			 styleButton1 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url("+ url +");background-size:100px 100px;background-repeat: no-repeat;";
	      }
	      if (imageNumberButton1 == 100){
	      	 var url = "./img/timer/TimerV2.00" + imageNumberButton1 + ".png?t=" + new Date().getTime();

	         styleButton1 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url("+ url +");background-size:100px 100px;background-repeat: no-repeat;";
	         imageNumberButton1 = 0;
	      }

          var imgSensor1 = new Image();
          imgSensor1.src = url;

          imgSensor1.onload = function(){ // Loaded successfully

	      		document.getElementById('UCIBed1').setAttribute("style", styleButton1);
	      };

	      imgSensor1.onerror = function(){ // Failed to load
              console.log("failed to load");
          };

	      document.getElementById('UCIBed1').childNodes[0].nodeValue = "00:00:" + imageNumberButton1;
		  
	}

	// Button timer 2
	function setProperties_UCIBed2(){

		  imageNumberButton2 = imageNumberButton2 + 1;

		  // Carga imagen sensor 1

	      if (imageNumberButton2 < 10){
	      	 var url = "./img/timer/TimerV2.000" + 0 + imageNumberButton2 + ".png?t=" + new Date().getTime();

			 styleButton2 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url("+ url +");background-size:100px 100px;background-repeat: no-repeat;";

	      }else{

	      	 var url = "./img/timer/TimerV2.000" + imageNumberButton2 + ".png?t=" + new Date().getTime();

			 styleButton2 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url("+ url +");background-size:100px 100px;background-repeat: no-repeat;";
	      }
	      if (imageNumberButton2 == 100){
	      	 var url = "./img/timer/TimerV2.00" + imageNumberButton2 + ".png?t=" + new Date().getTime();

	         styleButton2 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url("+ url +");background-size:100px 100px;background-repeat: no-repeat;";

	         imageNumberButton2 = 0;
	      }
	      var imgSensor1 = new Image();
          imgSensor1.src = url;
	      
	      imgSensor1.onload = function(){ // Loaded successfully
	      	document.getElementById('UCIBed2').setAttribute("style", styleButton2);
	      };

	      imgSensor1.onerror = function(){ // Failed to load
              console.log("failed to load");
          };

	      document.getElementById('UCIBed2').childNodes[0].nodeValue = "00:00:" + imageNumberButton2;
		  
	}

	// Button timer 3
	function setProperties_UCIBed3(){

		  imageNumberButton3 = imageNumberButton3 + 1;

		  // Carga imagen sensor 1

	      if (imageNumberButton3 < 10){

	      	 var url = "./img/timer/TimerV2.000" + 0 + imageNumberButton3 + ".png?t=" + new Date().getTime();

			 styleButton3 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url("+ url +");background-size:100px 100px;background-repeat: no-repeat;";

	      }else{
	      	 var url = "./img/timer/TimerV2.000" + imageNumberButton3 + ".png?t=" + new Date().getTime();

			 styleButton3 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url("+ url +");background-size:100px 100px;background-repeat: no-repeat;";
	      }
	      if (imageNumberButton3 == 100){

	      	 var url = "./img/timer/TimerV2.00" + imageNumberButton3 + ".png?t=" + new Date().getTime();

	         styleButton3 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url("+ url +");background-size:100px 100px;background-repeat: no-repeat;";
	         
	         imageNumberButton3 = 0;
	      }

	      var imgSensor1 = new Image();
          imgSensor1.src = url;

	      imgSensor1.onload = function(){ // Loaded successfully

	      	document.getElementById('UCIBed3').setAttribute("style", styleButton3);

	      };

	      document.getElementById('UCIBed3').childNodes[0].nodeValue = "00:00:" + imageNumberButton3;
		  
	}

	// Button timer 4
	function setProperties_UCIBed4(){

		  imageNumberButton4 = imageNumberButton4 + 1;

		  // Carga imagen sensor 1

	      if (imageNumberButton4 < 10){

	      	 var url = "./img/timer/TimerV2.000" + 0 + imageNumberButton4 + ".png?t=" + new Date().getTime();

			 styleButton4 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url("+ url +");background-size:100px 100px;background-repeat: no-repeat;";

	      }else{

	      	 var url = "./img/timer/TimerV2.000" + imageNumberButton4 + ".png?t=" + new Date().getTime();

			 styleButton4 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url("+ url +");background-size:100px 100px;background-repeat: no-repeat;";
	      }
	      if (imageNumberButton4 == 100){
	      	 var url = "./img/timer/TimerV2.00" + imageNumberButton4 + ".png?t=" + new Date().getTime();

	         styleButton4 = "width:450px;height:100px; color:#FFF; font-size:25px; border-radius: 10px;background: #000 url("+ url +");background-size:100px 100px;background-repeat: no-repeat;";
	         
	         imageNumberButton4 = 0;
	      }
	      var imgSensor1 = new Image();
          imgSensor1.src = url;
          
          imgSensor1.onload = function(){ // Loaded successfully

	      	document.getElementById('UCIBed4').setAttribute("style", styleButton4);

	      };

	      document.getElementById('UCIBed4').childNodes[0].nodeValue = "00:00:" + imageNumberButton4;
		  
	}

</script>
                    
</html>

