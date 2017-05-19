<?php
class Database{
    public static $db;
    private static $dsn = 'mysql:host=35.189.168.6;dbname=inspiringquotes';
    private static $username ='root';
    private static $passwd = '10041989';
}

public static function connect(){
    if(!isset(self::$db)){
        try{
            self::$db = new PDO(self::$dsn,self::$username,self::$passwd);
            self::$db ->exec('set names utf-8');
        }
        catch(PDOException $e)
        {
            echo $e->getMessage();
        }
        return self::$db;
    }
}