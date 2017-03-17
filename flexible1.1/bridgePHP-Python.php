<?php

    if (isset($_POST['id'])) {

        function deleteClient11($x) {
           return($x);
        }

        $parametro = deleteClient11($_POST['id']);

        $salida= array(); //recogerá los datos que nos muestre el script de Python
  
        //el argumento lleva la ruta de la sección de audio que se quiere comparar.
   
        $argumento=$parametro;  
    
        exec("python receptorClientPython.py '".$argumento."'",$salida);  

        print_r($salida);

    }

?>