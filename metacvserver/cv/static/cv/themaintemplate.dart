import 'dart:convert' show JSON;
import 'dart:html' show Element, window, querySelector, Event, HttpRequest,
NodeTreeSanitizer, LinkElement;
import 'package:metacvserver_common/openclose.dart' show StateManager;

String getURL(String hashtagid, [String featureid]){
  String url = "/"+hashtagid+"/";
  if(featureid != null){
    url = url+featureid+"/"; 
  }

  return url;
}

/*Loads data from the server and enter it in the Open Hashtag State
The only object with whom we interact on the page, since it also call the StateManager
*/
class OpenHashtagManager{
  String current_hashtag_id;
  String current_feature_id;
  String next_feature_id;
  
  StateManager statemanager;

  OpenHashtagManager(StateManager statemanager){
    this.statemanager = statemanager;

    this.current_hashtag_id = null;
    this.current_feature_id = null;
    this.next_feature_id = null;

    statemanager.close();
  }

  //MANAGEMENT METHODS

  /*Switch to the Open Hashtag State, 
    change the current hashtag,
    set the name,
    ask for the first feature and load it
  */
  void _loadHashtag(Map hashtagjson){

    this.current_hashtag_id = hashtagjson['id'];
    this.next_feature_id = hashtagjson['first_feature'];
    querySelector("#hashtag_title").text = hashtagjson['id'];
    
    window.history.replaceState("cityoftinylight", "", getURL(hashtagjson['id']));
    
    this.nextFeature();
  } 

  /*Set the current feature's id
    Set the feature body,
    Set the "next" url and id
  */
  void _loadFeature(Map featurejson){
    this.current_feature_id = featurejson['id'];
    querySelector("#feature_representation").setInnerHtml(
        featurejson['representation'], 
        treeSanitizer : NodeTreeSanitizer.trusted
    );
    create_showMore(querySelector("#feature_representation"));
    
    if(featurejson['next_feature_id'] != "CLOSE"){
      this.next_feature_id = featurejson['next_feature_id']; 
    } else {
      this.next_feature_id = null;
    }
    LinkElement linknext = querySelector("#next_hashtag");

    if(this.next_feature_id != null){
      linknext.href = this.next_feature_id;
    } else {
      linknext.href = "/";
    }
    window.history.replaceState("cityoftinylight", "", getURL(this.current_hashtag_id, this.current_feature_id));
    statemanager.open();
  }

  void closeHashtag(){
    this.statemanager.close();

    this.current_hashtag_id = null;
    this.current_feature_id = null;
    this.next_feature_id = null;

    window.history.replaceState("cityoftinylight", "", "/");
  }

  /*If next is none : switch to the Main Screen State
    Otherwise : load the next feature*/
  void nextFeature(){
    if(this.next_feature_id == null){
      this.closeHashtag();
    } else {
      Map<String, String> httpheader = new Map<String,String>();
      httpheader['X-Requested-With'] = 'XMLHttpRequest';
      HttpRequest.request(getURL(this.current_hashtag_id, this.next_feature_id), requestHeaders:httpheader)
        .then((HttpRequest featurejson_raw){
          Map featurejson = JSON.decode(featurejson_raw.response);
          this._loadFeature(featurejson);
      });
    }
  }


  void showHashtag(String hashtag_id){
    Map<String, String> httpheader = new Map<String,String>();
    httpheader['X-Requested-With'] = 'XMLHttpRequest';
    HttpRequest.request(getURL(hashtag_id), requestHeaders:httpheader)
      .then((HttpRequest hashtagjson_raw) {
        Map hashtagjson = JSON.decode(hashtagjson_raw.response);
        this._loadHashtag(hashtagjson);
      });
  }
  
  //To load a hashtag on startup, without ajax
  void showHashtag_noajax(String id, String first_feature_id){
    Map hashtagjson = new Map();
    hashtagjson['id'] = id;
    hashtagjson['first_feature'] = first_feature_id;

    _loadHashtag(hashtagjson);
  }
}

void create_showMore(Element feature_representation){
    Element more_btn = feature_representation.querySelector(".employer .more_btn");
    if(more_btn != null){
        more_btn.onClick.listen(
            (Event e){
                e.preventDefault(); 
                feature_representation.querySelectorAll(".more_btn ~ .hidden").forEach(
                    (Element e){
                        e.classes.remove("hidden");
                    }
                );
                more_btn.classes.add("hidden");
            }
        );
    }
}
