package com.orleven.tentacle.commun;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;

/**
 * web 控制层 ,用来服务器间的交流
 * @author orleven
 * @date 2017年3月8日
 */
@RestController
public class Communication {

    @RequestMapping(value="/index",method = RequestMethod.GET)
    public String index(){
        return "hello";
    }

    @RequestMapping(value="/getPath",method=RequestMethod.POST)
    public String getPath(HttpServletRequest request){
        return request.getParameter("rootPath");
    }

    @RequestMapping(value="/getStatus/{id}",method=RequestMethod.GET)
    public String getStatus(@PathVariable int id){
        return ""+id;
    }

    @RequestMapping(value="/setTask")
    public String setTask(){
        return "";
    }
    
    @RequestMapping(value="/startMonitor/{taskName}",method=RequestMethod.GET)
    public String startMonitor(@PathVariable String taskName){

    	return "Success ! ";
    }

}
