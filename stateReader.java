import java.awt.image.*;
import java.io.*;
import java.util.*;
import javax.imageio.ImageIO;
import java.awt.Color;
public class stateReader
{
  static ArrayList<Color> visitedProvinces = new ArrayList<Color>();
  static ArrayList<Color> visitedStates = new ArrayList<Color>();
  static ArrayList<Integer> provinceIndexes = new ArrayList<Integer>();
  static ArrayList<ArrayList<Integer>> colours = new ArrayList<ArrayList<Integer>>(); 
  static ArrayList<String[]> csvData = new ArrayList<String[]>();
  static BufferedImage states, provinces;
  static int index;
  static Color stateColor, provinceColor;
  static FileWriter fw;
  final static Color BLACK = new Color(0,0,0);
  
  public static void csvReader()
  {
    String row;
    BufferedReader csvReader;
    try
    {
      csvReader = new BufferedReader(new FileReader("definition.csv"));
      while ((row = csvReader.readLine()) != null) 
      {
        csvData.add(row.split(";"));
      }
    }
    catch(Exception e)
    {
      System.out.println("File Error");
    }
  }
      
  
  
  public static void main(String[] args)
  {
    
    csvReader();
    
    try
    {
      states=ImageIO.read(new File("states.png"));
    }
    catch(Exception e)
    {
      System.out.println("File not found");
    }
    try
    {
      provinces=ImageIO.read(new File("provinces.png"));
    }
    catch(Exception e)
    {
      System.out.println("File not found");
    }
    
    
    
    for (int i=0;i<states.getHeight();i++)
    {
      System.out.println((100*i)/states.getHeight()+"%");
      
      for (int j=0;j<states.getWidth();j++)
      {
        stateColor=new Color(states.getRGB(j,i),true);
        if(!stateColor.equals(BLACK))
        {
          provinceColor=new Color(provinces.getRGB(j,i),true);
          index=visitedStates.indexOf(stateColor);
          
          if(index<0)
          {
            visitedStates.add(stateColor);
            colours.add(new ArrayList<Integer>());
            index=visitedStates.size()-1;
          }
          
          if(visitedProvinces.indexOf(provinceColor)<0)
          {
            visitedProvinces.add(provinceColor);
            
            for(String[] s:csvData)
            {
              if(Integer.parseInt(s[1])==provinceColor.getRed()&&Integer.parseInt(s[2])==provinceColor.getGreen()&&Integer.parseInt(s[3])==provinceColor.getBlue())
              {
                colours.get(index).add(Integer.parseInt(s[0]));
                break;
              }
            }
            
          }
          
        }
      }
    }
    for(int i=0;i<colours.size();i++)
    {
      try 
      {
        
        fw = new FileWriter(new File(Integer.toString(i)+"-"+Integer.toString(visitedStates.get(i).getRed())+","+Integer.toString(visitedStates.get(i).getGreen())+","+Integer.toString(visitedStates.get(i).getBlue())+".txt"));
        
        fw.write("state={\n");
        fw.write("\tid="+i+"\n");
        fw.write("\tname=\"STATE_"+i+"\" # \n");
        fw.write("\tmanpower = \n\n");
        fw.write("\tstate_category = \n\n");
        fw.write("\thistory={\n");
        fw.write("\t\towner = \n");
        fw.write("\t\tvictory_points = { }\n");
        fw.write("\t\tbuildings = {\n");
        fw.write("\t\t\tinfrastructure =\n");
        fw.write("\t\t\tindustrial_complex =\n");
        fw.write("\t\t\tarms_factory =\n");
        fw.write("\t\t\tdockyard =\n");
        fw.write("\t\t}\n");
        fw.write("\t\tadd_core_of =\n");
        fw.write("\t}\n");
        fw.write("\tprovinces={\n");
        
        fw.write("\t\t");
        for(int j:colours.get(i))
        {
          fw.write(j+" ");
        }
        fw.write("\n");
        
        fw.write("\t}\n");
        fw.write("}");
        fw.close();
        
      } 
      catch (IOException ex) 
      {
        ex.printStackTrace();
      }
      
    }
  }
}