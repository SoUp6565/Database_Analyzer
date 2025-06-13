import java.io.*;
import java.net.URL;
import java.sql.*;
import java.util.ArrayList;
import java.util.Scanner;


//  ### = PRIVATE INFOS
public class DatabaseExplorer {
    static String url="jdbc:sqlserver://IPSERVER\\SQLEXPRESS;databaseName=DBNAME;encrypt=true;trustServerCertificate=true";
    static String name="yourname";
    static String password="yourpassword";
    static ArrayList<Integer> thirtys = new ArrayList<>();

    static ArrayList<Integer> thirtyones = new ArrayList<>();


    public static void main(String[] args) throws SQLException, IOException {

        Connection connection= DriverManager.getConnection(url,name,password);
        System.out.println("Connessione ok"+'\n');
        Statement statement= connection.createStatement();
        ResultSet resultSet=null;
        thirtys.add(4);
        thirtys.add(6);
        thirtys.add(9);
        thirtys.add(11);
        thirtyones.add(1);
        thirtyones.add(3);
        thirtyones.add(5);
        thirtyones.add(7);
        thirtyones.add(8);
        thirtyones.add(10);
        thirtyones.add(12);
        String startingYear;
        String finalYear;
        Scanner scanner=new Scanner(System.in);
        System.out.println("Inserire l'intervallo di tempo da analizzare in anni (>4 anni protrebbe riempire l'heap, fermando il programma ) ");
        startingYear=scanner.nextLine();
        finalYear=scanner.nextLine();
            int years=Integer.parseInt(startingYear);
            int yearsLimit=Integer.parseInt(finalYear);
            int nDay=1;
            int nMonth=1;
            int monthType;
            System.out.println("Analisi in corso...");
            while (true){
                if(thirtys.contains(nMonth)){
                    monthType=0;
                }
                else if(thirtyones.contains(nMonth)){
                    monthType=1;
                }
                else{
                    monthType=2;
                }
                String day;
                String month;
                if((nDay/10)==0){
                     day="0"+nDay;
                }
                else{
                     day=""+ nDay;
                }
                if((nMonth/10)==0){
                     month="0"+nMonth;
                }
                else{
                     month=""+ nMonth;
                }
            URL url = new URL("https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/dailyRates?referenceDate="+years+"-"+month+"-"+day+"&currencyIsoCode=EUR&lang=it");
            BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()));
            String line = reader.readLine();

            while (!line.isEmpty()) {
                String date;
                String code;
                String value;
                date = line.substring(line.lastIndexOf(',') + 1);
                line = line.substring(line.indexOf(',') + 1);
                line = line.substring(line.indexOf(',') + 1);
                code = line.substring(0, line.indexOf(','));
                line = line.substring(line.indexOf(',') + 1);
                line = line.substring(line.indexOf(',') + 1);
                value = line.substring(0, line.indexOf(','));
                DatabaseExplorer.insertData(connection, date, code, value);
                line = reader.readLine();

            }
            nDay++;
            switch (monthType){
                case 0:
                    if(nDay>30){
                        nDay=1;
                        nMonth++;
                    }
                    break;
                case 1:
                    if(nDay>31){
                        nDay=1;
                        nMonth++;
                    }
                    break;
                case 2:
                    if(nDay>28){
                        nDay=1;
                        nMonth++;
                    }
                    break;
            }
            if(nMonth>12){
                years++;
                nMonth=1;

            }
            if(years>yearsLimit){
                break;
            }
    }
        printDatabase(connection,resultSet);
        statement.close();
        connection.close();
    }

    public static void printDatabase(Connection connection,ResultSet resultSet) throws SQLException {
        resultSet=connection.createStatement().executeQuery("SELECT ### FROM ###");
        boolean hasNext=false;
        try {
            hasNext = resultSet.next();
        }
        catch (Exception e){
            System.out.println(e.getMessage());
        }
        if(!hasNext){
            System.out.println("Database vuoto");
            return;
        }
        else {
            System.out.println("Contenuto database:");
        }
        do{
            System.out.print(resultSet.getString("###")+" ; ");
            System.out.print(resultSet.getString("###")+" ; ");
            System.out.println(resultSet.getString("###"));
            hasNext= resultSet.next();
        }
        while(hasNext);
    }
    static void insertData(Connection connection,String date,String code,String value) throws SQLException {
        if(code.equals("Codice ISO")){
            return;
        }
        try {
            PreparedStatement pS2= connection.prepareStatement("SELECT ### FROM ### WHERE ### = ? AND ### = ?");
            pS2.setString(1,date);
            pS2.setString(2,code);

            try (ResultSet rs = pS2.executeQuery()) {
                if (rs.next()) {
                    int count = rs.getInt(1);
                    if (count > 0) {
                        return;
                    }
                }
            }
        catch (SQLException e) {
            System.out.println(e);
        }


        PreparedStatement preparedStatement=connection.prepareStatement("INSERT INTO ### (###, ###, ###) VALUES (?, ?, ?)");
            preparedStatement.setString(1,date);
            preparedStatement.setString(2,code);
            preparedStatement.setString(3,value);
            preparedStatement.executeUpdate();
        } catch (Exception e) {
            System.out.println(e);
        }
    }

    static void deleteDataByDate(Connection connection,String date){
        try{
            PreparedStatement preparedStatement= connection.prepareStatement("DELETE FROM ### WHERE ### = ?");
            preparedStatement.setString(1,date);
            preparedStatement.executeUpdate();
            preparedStatement.close();

        } catch (SQLException e) {
            System.out.println("COULDNT DELETE ROW");
        }
    }

}
