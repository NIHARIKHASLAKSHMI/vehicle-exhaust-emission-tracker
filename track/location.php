<?php

extract($_REQUEST);


$fp=fopen("loc.txt","w");
fwrite($fp,$loc);
fclose($fp);

?>
