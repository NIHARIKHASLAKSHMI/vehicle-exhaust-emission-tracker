<?php

extract($_REQUEST);

$loc=$lat.", ".$lon;

$fp=fopen("loc.txt","w");
fwrite($fp,$loc);
fclose($fp);
?>