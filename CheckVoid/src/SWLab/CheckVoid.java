package SWLab;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
public class CheckVoid {

	public static boolean checkVoid(String path, String content){
		
		if(content != null)
			if(content.contains("dataset"))
				return false;
		Model model = ModelFactory.createDefaultModel();
		try{model.read(path);
		return model.toString().contains("void:Dataset");
		}
		catch(Exception e){
			return false;
		}
		
	}

}
