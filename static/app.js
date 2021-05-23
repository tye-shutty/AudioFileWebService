// import axios from 'axios';
// Vue.use(axios);
var app = new Vue({
  el: "#app",

  //------- global data --------
  data: {
    domain: 'tyeshutty.tk',
    serviceURL: "/audio",
    //"", //"http://ec2-18-218-32-161.us-east-2.compute.amazonaws.com", //"https://cs3103.cs.unb.ca:5045",
    authenticated: false,
    email: "",
    admin_status: {user: {}},
    input: {
      username: "",
      password: ""
    },
    folder_input: {
      name: "",
      description: "",
      parent: 0
    },
    folders: [],
    edit_folder: null,
    show_folder: 0,
    show_folder_name: "",
    show_folder_description: "",
    files: [],
    file_input: {
      description: "",
      parent: 0,
      file: null,
      plays_count: null,
      last_played: null
    },
    edit_file: null,
    add_folder: false,
    add_folder_icon: "⇈",
    add_file_icon: "⇈",
    add_file: false,
    mod_folder: null,
    set_folder: false,
    set_file: false,
    sound: {},
    show_file: null,
    info: false,
    about_icon: "⇈",
    search: "",
    searched: false,
    searched_string: "",
    users: [],
    target_user: "",
    toggle_users: false,
    add_file_complete: true,
    add_folder_complete: true,
    target_input_valid: false,
    signup_success: false,
    signup_failure: false,
    signin_failure: false,
    last_signin_email: "",
    last_signin_password: "",
    last_signup_email: "",
    last_signup_password: "",
    warning: false,
    warning_message: "",
    version: 'may23'
  },
  methods: {
    login() {
      v=this;
      if(v.input.username === "" || v.input.password === ""){
        v.warning = true;
        v.warning_message = "email and password must be at least 1 character long"
        return;
      }
      v.warning = false;
      v.input.username = v.input.username.toLowerCase();
      if(v.last_signin_email == v.input.username && v.last_signin_password == v.input.password){
        return;
      }
      this.signup_success = false;
      this.signup_failure = false;
      v.last_signin_email = v.input.username;
      v.last_signin_password = v.input.password;
      if(v.domain == 'cs3103.cs.unb.ca'){
        axios
        .post(v.serviceURL+"/signin", {
            "email": v.input.username,
            "password": v.input.password
        })
        .then(response => {
            if (response.data.status == "success") {
              if(!navigator.userAgent.includes('Firefox') ){
                alert('Site will behave poorly on non-Firefox browsers');
              }
              mobileCheck = function() {
                let check = false;
                (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
                return check;
              };
              c = mobileCheck();
              alert('mob check= '+c);
              if(c){
                alert("Site doesn't work on mobile");
              }
              v.authenticated = true;
              // console.log(response.status);
              axios 
              .post(v.serviceURL+"/users", {
                "email": v.input.username + "@unb.ca"
              })
              .then(response2 => {
                if (response2.status == 201) {
                  //console.log('response=',response2);
                  v.email = v.input.username + "@unb.ca";
                  v.target_user = v.email;

                axios 
                .get(v.serviceURL+"/users/"+v.email)
                .then(response3 => {
                  console.log("user data 201 =",response3.data);
                  v.admin_status = response3.data; //.user.admin_status;
                  v.getFolders();
                })
                .catch(e => {
                  console.log(e);
                });
                  }
              })
              .catch(e => {
                // if(!(response in e)){
                //   console.log("no response in 409!");
                // }
                if((e.response)){
                  console.log("response in 409!")
                  console.log(e.response, e.response.data);
                }
                console.log('409 err=',e);
                if (e.response && e.response.status == 409) {
                  console.log("things work",e.response, e.response.data, e.response.status);
                  this.email = this.input.username + "@unb.ca";
                  this.target_user = this.email;

                  axios 
                  .get(this.serviceURL+"/users/"+this.email)
                  .then(response4 => {
                    console.log("user data 409=",response4.data);
                    console.log("user data.user 409=",response4.data.user.admin_status);
                    v.admin_status = response4.data; //.user.admin_status;
                    this.getFolders();
                  })
                  .catch(e => {
                    //console.log(e);
                  });
                }
              });
            }
        })
        .catch(e => {
            alert("The username or password was incorrect, try again");
            this.input.password = "";
            console.log(e.response);
        });
      }
      else{ //not using UNB system
        axios
        .post(this.serviceURL+"/signin", {
            "email": this.input.username,
            "password": this.input.password
        })
        .then(response => {
          if (response.data.status == "success") {
            if(!navigator.userAgent.includes('Firefox')){
              alert('Site will behave poorly on non-Firefox browsers');
            }
            mobileCheck = function() {
              let check = false;
              (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
              return check;
            };
            c = mobileCheck();
            if(c){
              alert("Site doesn't work on mobile");
            }
            v.last_signin_email = '';
            v.last_signin_password = '';
            this.signin_failure = false;
            this.authenticated = true;
            this.email = this.input.username;
            this.target_user = this.email;
            axios 
            .get(this.serviceURL+"/users/"+this.email)
            .then(response3 => {
              console.log("user data 201 =",response3.data);
              v.admin_status = response3.data; //.user.admin_status;
              this.getFolders();
            })
            .catch(e => {
              console.log(e);
            });
          }
        })
        .catch(_ => {
          this.signin_failure = true;
        });
      }
    },
    logout() {
      axios
      .delete(this.serviceURL+"/signin")
      .then(response => {
          location.reload();
          
      })
      .catch(e => {
        console.log(e.response);
      });
    },
    fetchUser(){
      if(this.email != ""){
      }
    },
    addFolder() {
      if(this.target_user != ""){
        axios
        .post(this.serviceURL+"/users/"+this.target_user+"/folders", {
          "folder_name": this.folder_input.name,
          "folder_description": this.folder_input.description,
          "parent": this.show_folder
        })
        .then(response => {
          // console.log(response);
          this.getFolders();
          this.add_folder_complete=true;
        })
        .catch(e => {
          console.log(e.response);
          this.add_folder_complete=true;
        });
      }
    },
    getFolders(){
      // console.log("getting folders", this.email);
      if(this.target_user != ""){
        let str = (this.search === "" ? "%" : this.search);
        // if(this.email !== this.target_user){
        //   this.show_folder=0;
        // }
        // console.log("searching", str);
        axios
        .get(this.serviceURL+"/users/"+this.target_user+"/folders", {params: {string: str}})
        .then(response => {
          this.searched_string = this.search;
          this.folders = [];
          promises = [];
          for(const folder in response.data.folders){
            promises.push(axios.get(this.serviceURL+"/users/"+this.target_user+"/folders/"+response.data.folders[folder]["folder_id"]));
          }
          Promise.all(promises)
          .then(responses => {
            console.log("promised responses=",responses);
            for(const response in responses){
              let folder = responses[response].data.folder;
              this.folders.push(folder);
            }
            function compare(me, you){
              if("folder_id" in me && "folder_id" in you){
                return you["folder_id"] - me["folder_id"]; //if negative or 0, doesn't swap (descending) 
              }
            }
            this.folders.sort(compare);
          })
          .catch(e => {
            console.log(e.response);
          });
        })
        .catch(e => {
          console.log(e);
        });
      }
    },
    setFolder(id){
      if(this.target_user != ""){
        // console.log(id);
        axios
        .patch(this.serviceURL+"/users/"+this.target_user+"/folders/"+this.edit_folder, {
          "name": this.folder_input.name,
          "description": this.folder_input.description
        })
        .then(response => {
          //console.log(response);
          this.edit_folder = null;
          this.getFolders();
        })
        .catch(e => {
          console.log(e.response);
        });
      }
    },
    deleteFolder(id){
      if(this.target_user != ""){
        // console.log(id);
        axios
        .delete(this.serviceURL+"/users/"+this.target_user+"/folders/"+id)
        .then(response => {
          //console.log(response);
          this.getFolders();
        })
        .catch(e => {
          console.log(e.response);
          // this.fail_delete=id; 
          alert("Can't delete folder with contents");
        });
      }
    },
    handleFileUpload(){
      this.file_input.file = this.$refs.file.files[0];
    },
    addFile() {
      if(this.target_user != ""){
        // this.file_input.file = this.$refs.file.files[0];
        var bodyFormData = new FormData();
        bodyFormData.append("file_description", this.file_input.description);
        bodyFormData.append("parent", this.show_folder);
        bodyFormData.append("file", this.file_input.file);
        // console.log(this.file_input);
        axios({
          method: "post",
          url: this.serviceURL+"/users/"+this.target_user+"/files",
          data: bodyFormData,
          headers: { "Content-Type": "multipart/form-data" }
        })
        .then(response => {
          this.getFiles();
          this.pauseAll();
          this.add_file_complete=true;
          //console.log(response);
        })
        .catch(e => {
          console.log(e.response);
          this.add_file_complete=true;
        });
      }
    },
    getFiles(){
      if(this.target_user != ""){

        let str = (this.search === "" ? "%" : this.search);
        // console.log("searching", str);
        axios
        .get(this.serviceURL+"/users/"+this.target_user+"/files", {params: {string: str}})
        .then(response => {
          this.files = [];
          promises = [];
          // console.log(response);
          // console.log(response.data.files);
          for(const file in response.data.files){
            promises.push(axios.get(this.serviceURL+"/users/"+this.target_user+"/files/"+response.data.files[file]["file_id"]));
          }
          Promise.all(promises)
            .then(responses => {
              // console.log("responses=",responses);
              for(const response in responses){
                // console.log("file=",responses[response].data.file);
                let file = responses[response].data.file;
                this.files.push(file);
                this.files[this.files.length-1].seek_percent = 0;
                this.files[this.files.length-1].volume = 100;
                this.files[this.files.length-1].paused_proposition = "play "
                this.files[this.files.length-1].last_played_locale = new 
                Date(this.files[this.files.length-1].last_played).toLocaleString();
                // console.log("new local=",this.files[this.files.length-1].last_played_locale);
                if(this.files[this.files.length-1].last_played_locale === "Invalid Date"){
                  this.files[this.files.length-1].last_played_locale = "Never Played";
                }
                this.files[this.files.length-1].upload_date_locale = new 
                Date(this.files[this.files.length-1].upload_date).toLocaleString();

                var date = new Date(this.files[this.files.length-1].last_played);
                // "yyyy-MM-dd hh:mm TT"
                //must be converted in mysql friendly format
                date_str = date.getUTCFullYear() + '-' +
                  ('00' + (date.getUTCMonth()+1)).slice(-2) + '-' +
                  ('00' + date.getUTCDate()).slice(-2) + ' ' + 
                  ('00' + date.getUTCHours()).slice(-2) + ':' + 
                  ('00' + date.getUTCMinutes()).slice(-2) + ':' + 
                  ('00' + date.getUTCSeconds()).slice(-2);
                this.files[this.files.length-1].last_played = date_str;
                function compare(me, you){
                  // console.log("init compare",me,you);
                  if("file_id" in me && "file_id" in you){
                    // console.log("comparing ",you["file_id"], me["file_id"]);
                    return you["file_id"] - me["file_id"]; //if negative or 0, doesn't swap (descending) 
                  }
                }
                this.files.sort(compare);
              }
            })
            .catch(e => {
              console.log(e.response);
            });
        })
        .catch(e => {
          console.log(e.response);
        });
      }
    },
    deleteFile(id){
      if(this.target_user != ""){
        // console.log(id);
        this.pause(id);
        axios
        .delete(this.serviceURL+"/users/"+this.target_user+"/files/"+id)
        .then(response => {
          //console.log("delete resp=",response);
          this.getFiles();
          this.pauseAll();
        })
        .catch(e => {
          console.log(e.response);
          // this.fail_delete=id; 
        });
      }
    },
    setFile(id){
      if(this.target_user != ""){
        // console.log("searching",id);
        for(const x in this.files){
          // console.log("parsing",this.files[x]);
          if (this.files[x].file_id == id){
            var prev = this.files[x];
          }
        }
        //console.log('prev=',prev);
        axios
        .patch(this.serviceURL+"/users/"+this.target_user+"/files/"+this.edit_file, {
          "name": this.file_input.name,
          "description": this.file_input.description,
          "plays_count": prev.times_played,
          "last_played": prev.last_played,
          "parent": prev.parent
        })
        .then(response => {
          //console.log("set response=",response);
          this.getFiles();
          this.edit_file = null;
          this.pauseAll();
        })
        .catch(e => {
          console.log(e.response);
        });
      }
    },
    display_add_folder(){
      this.add_folder=!this.add_folder;
      if(this.add_folder===true){
        this.add_folder_icon = "⇊";
      } else{
        this.add_folder_icon = "⇈";
      }
    },
    display_add_file(){
      this.add_file=!this.add_file;
      if(this.add_file===true){
        this.add_file_icon = "⇊";
      } else{
        this.add_file_icon = "⇈";
      }
    },
    getFileName(id,short){
      for(const x in this.files){
        if (this.files[x].file_id === id){
          // console.log('file=',this.files[x].file_name)
          ret = this.files[x].file_name;
          if(short ===true){
            ret = ret.substring(0,20);
          }
          return ret;
        }
      }
      return "your_file"
    },
    getFolderName(id,short){
      if(id===0){
        return "Home Directory"
      }
      for(const x in this.folders){
        if (this.folders[x].folder_id === id){
          ret = this.folders[x].folder_name;
          if(short ===true){
            // console.log("ret=", ret, ret.length);
            ret = ret.substring(0,20);
            ret = ret + " ".repeat(20-ret.length);
            // console.log(ret);
          }
          return ret;
        }
      }
      return id
    },
    getHeaderName(){
      if(this.show_folder===0){
        this.show_folder_name = "Home Directory";
      }
      ret = this.searched===false ? "Viewing "+ this.show_folder_name : "Search results of '"+this.searched_string+"'";
      return ret + this.adminTitle();
    },
    getFolderDescription(id){
      if(id===0){
        return;
      }
      for(const x in this.folders){
        if (this.folders[x].folder_id === id){
          return this.folders[x].folder_description;
        }
      }
      return id;
    },
    getFileName(id,short){
      for(const x in this.files){
        if (this.files[x].file_id === id){
          ret = this.files[x].file_name;
          if(short ===true){
            // console.log("ret=", ret, ret.length);
            ret = ret.substring(0,25);
            ret = ret + " ".repeat(25-ret.length);
            // console.log(ret);
          }
          return ret;
        }
      }
      return id
    },
    play(id, file){
      if(!(id in this.sound)){
        // axios
        //   .get(this.serviceURL+"/users/"+this.email+"/files/"+file.file_id, 
        //   {params: {stream: true}})
        //   .then(response => {
        //     console.log("file stream=",response);
        //     this.sound[id] = new Audio(response.data);
        //   })
        //   .catch(e => {
        //     console.log(e.response);
        //   });
        this.sound[id] = new Audio(this.serviceURL+"/users/"+this.target_user+"/files/"+file.file_id+"?stream=true");
      }
      // console.log(this.sound[id].canPlayType("audio/wav"), this.sound[id].canPlayType("audio/ogg"), this.sound[id].canPlayType("audio/mpeg"));
      // if(this.sound[id].canPlayType("audio/wav") != "probably" &&
      // this.sound[id].canPlayType("audio/ogg") != "probably" &&
      // this.sound[id].canPlayType("audio/mpeg") != "probably")
      // {
      //   alert('not playable');
      // }
      vm = this;

      function update_seeker(last, sound) {
        // console.log('info=',sound.currentTime, sound.duration);
        if((isNaN(sound.currentTime) || sound.currentTime != last) &&
          (isNaN(sound.duration) || sound.currentTime < sound.duration))
        {
          let old_time = sound.currentTime;  //must be let or other calls to update_seeker will see each other's old_time
          setTimeout(
            function(){
              console.log('playing',file.seek_percent);
              file.seek_percent = (sound.currentTime / sound.duration)*100;
              // location.reload();
              // vm.componentKey2 += 1;
              // $("#event").load("#event");
              vm.$forceUpdate();
              update_seeker(old_time, sound);
            },
            500);
        } else if((isNaN(sound.currentTime) || isNaN(sound.duration)) ||
        sound.currentTime/sound.duration > 0.99)
        {
          file.seek_percent = 0;
          vm.paused_proposition = 'play';
          vm.$forceUpdate();
        }
      }
      function onceRunning(){  //"loadeddata"
        console.log("Audio data loaded");
        console.log("Audio duration: " + this.duration);
        vm.seek(id, file.seek_percent);
        vm.setVolume(id, file);
        update_seeker(-1,vm.sound[id]);

        if(vm.email != ""){
          var date = new Date();
          // "yyyy-MM-dd hh:mm TT"
          date_str = date.getUTCFullYear() + '-' +
              ('00' + (date.getUTCMonth()+1)).slice(-2) + '-' +
              ('00' + date.getUTCDate()).slice(-2) + ' ' + 
              ('00' + date.getUTCHours()).slice(-2) + ':' + 
              ('00' + date.getUTCMinutes()).slice(-2) + ':' + 
              ('00' + date.getUTCSeconds()).slice(-2);
          //console.log("new time",date_str, file.times_played + 1);
          file.times_played = file.times_played + 1;
          file.last_played_locale = date.toLocaleString(); //convert to local time
          file.last_played = date_str;
          axios
          .patch(vm.serviceURL+"/users/"+vm.email+"/files/"+file.file_id, {
            "name": file.file_name,
            "description": file.file_description,
            "plays_count": file.times_played,
            "last_played": date_str,
            "parent": file.parent
          })
          .then(response => {
            //console.log(response);
          })
          .catch(e => {
            console.log(e.response);
          });
        }
       }
      console.log("paused?",this.sound[id].paused, "readystate", this.sound[id].readyState);
      if(this.sound[id].paused===true){
        file.paused_proposition = "pause";
        this.sound[id].play();
        if(this.sound[id].readyState ==4){
          onceRunning();
        }
        this.sound[id].addEventListener("loadeddata", onceRunning);
      } else{
        file.paused_proposition = "play ";
        this.pause(id);
      }
    },
    pause(id){
      if(id in this.sound){
        this.sound[id].pause();
      }
    },
    seek(id, seek_percent){
      if(id in this.sound){
        time = (seek_percent/100)*this.sound[id].duration;
        console.log("seeking", time, seek_percent, this.sound[id].duration);
        if (!isNaN(time)){
          this.sound[id].currentTime = time;  //fastSeek is not supported on chrome
        }
      }
    },

    setVolume(id, file){
      if(file.volume === 0 || file.volume === "0"){
        newVol = 0;
      } else{
        newVol = (Math.pow(1.1, file.volume) - 1)/100;
      }
      if(newVol > 1){
        newVol = 1;
      }
      //console.log("setting vol", newVol);
      if(id in this.sound){
        this.sound[id].volume = newVol;
      }
    },
   pauseAll(){
    for(const sound_index in this.sound){
      this.sound[sound_index].pause();
    }
    for(const file in this.files){
      file.paused_proposition = 'play';
    }
    show_file = null;
   },
   getUsers(){
     if(this.toggle_users===false){
      console.log("getting users");
      if(this.admin_status.user.admin_status===1){
        axios 
        .get(this.serviceURL+"/users")
        .then(response => {
          if (response.status == 200) {
            console.log('user response=',response);
            this.users = response.data.users;
            // for (const i in response.data.users){
            //   this.users.push(response.data.users[i]);
            // }

          }
        })
        .catch(e => {
          console.log('getUsers error=',e);
        });
      }
      this.toggle_users = true;
    } else{
      this.toggle_users = false;
    }
  },
  setAdmin(admin_status){
    if(this.target_user != ""){
      // console.log(id);
      axios
      .patch(this.serviceURL+"/users/"+this.target_user+"/authorize", {
        "admin_status": admin_status
      })
      .then(response => {
        this.target_user = this.email;
        //console.log(response);
      })
      .catch(e => {
        console.log(e.response);
      });
    }
  },
  deleteUser(){
    if(this.target_user != ""){
      // for (const file in this.files){
      //   axios.delete(this.serviceURL+"/users/"+this.target_user+"/files/"+file.file_id)
      // }
      axios
      .delete(this.serviceURL+"/users/"+this.target_user)
      .then(response => {
        if(this.target_user == this.email){
          this.logout();
        } else{
          this.target_user = this.email;
        }
        //console.log(response);
      })
      .catch(e => {
        console.log(e.response);
      });
    }
  },
  adminTitle(){
    if(this.target_user !== this.email){
      return " in "+this.target_user;
    } else{
      return "";
    }
  },
  signup(){
    v=this;
    if(v.input.username === "" || v.input.password === ""){
      v.warning = true;
      v.warning_message = "email and password must be at least 1 character long"
      return;
    }
    v.warning = false;
    v.input.username = v.input.username.toLowerCase();
    if(v.last_signup_email == v.input.username && v.last_signup_password == v.input.password){
      return;
    }
    v.signin_failure = false;
    v.last_signup_email = v.input.username;
    v.last_signup_password = v.input.password;
    axios 
    .post(this.serviceURL+"/users", {
      "email": this.input.username,
      "password": this.input.password
    })
    .then(response2 => {
      if (response2.status == 201) {
        this.signup_success = true;
        this.signup_failure = false;
        v.last_signin_email = '';
        v.last_signin_password = '';
      }
    })
    .catch(_ => {
      this.signup_success = false;
      this.signup_failure = true;
    });
  }



  }//,
  //------- END methods --------
  // mounted:
  // function(){
  //   console.log('mountains');
  //   this.axios
  //   .get(this.serviceURL+"/signin")
  //   .then(response => {
  //     console.log("res",response);
  //   })
  //   .catch(e => {
  //     console.log("err",e.response);
  //   });
  // }
});
