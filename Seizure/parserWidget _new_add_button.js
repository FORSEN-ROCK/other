 var parser = {
            firstName:/(?:���.+?)([�-��-߸�]+)/g,
            lastName:/(?:�������.+?)([�-��-߸�]+)/g,
            middleName:/(?:��������.+?)([�-��-߸�]+)/g,
            sex:/(?:���.+?)(�������|�������)/g,
            Birth:/(?:���� ��������.+?)([0-3][0-9].[0-1][0-9].[0-9]+)/g,
            homePhone:/(?:���.+?)(8.\d{3}.\d{3}.\d{2}.\d{2})/g,
            jobPhone:/(?:���.+?.+?)(8.\d{3}.\d{3}.\d{2}.\d{2})/g,
            mobelPhone:/(?:���������|�������|���.|���..+)((\+7|8).\d{3}.\d{3}.\d{2}.\d{2})/g,
            email_1:/(?:E-mail.+?)(\w+@\w+\.\w{2,3})/g,
            email_1:/(?:E-mail.+?)(\w+@\w+\.\w{2,3})/g,
            skype:/(?:Skype.+?)([0-9a-zA-Z]+)/g,
            city:/(?:�����.+?)([�-��-߸�]+)/g,
            address:/(?:�����.+?)(��.+?[�-���-ߨ]+.+? ���.+?[0-9].+)/g,
            region:/(?:������.+?)([0-9�-���-ߨ].+)+/g,
            metroStation:/(?:������� �����.+?)([0-9�-���-ߨ].+)+/g,
            education:/(?:�����������.+?)([�-��-߸�a-zA-Z].+)+/g,
            jobTitle:/(?:�������� ���������.+?)([�-��-߸�a-zA-Z].+)+/g,
            jobPay:/(?:��������.+?)([0-9]+.+? ���|���|���|���|���|���|Rub|rub|y.e)/g,
            experience:/(?:����.+?)([0-9]+.+?���.+?[0-9]+.+�������)/g,
            specialty:/(?:�������������.+?)([�-��-߸�a-zA-Z].+)+/g,
            rating:/./g
            
        }
        var selection = ""; // ����������� ������
        function handlerClick(event) {
            var target = event.target;
            if(target.dataset.comand == undefined) {
                return;
            }
            switch(target.dataset.comand) {
                case "parse":
                    var textContain = document.querySelector("textarea");
                    var dataString = textContain.value;
                    if(dataString == "") {
                        return;
                    }
                    var parserForm = document.forms[0];
                    for(var key in parser){
                        var itemParse = parser[key].exec(dataString);
                        if(itemParse.length != 0){
                            parserForm[key].value = itemParse[1];//dataString.match(parser[key][1]);
                            //console.log(''+ key + ' => ' + parser[key].exec(dataString));
                        }
                    }
                    break;
                    
                case "textField":
                    selection = "";//���������� ������
                    var currentActionElem = document.activeElement;
                    if(currentActionElem.tagName == "TEXTAREA"){
                        selection = currentActionElem.value.substring(currentActionElem.selectionStart, currentActionElem.selectionEnd);
                    }
                    break;
                    
                case "fillField":
                    if(!event.ctrlKey){
                        return;
                    }
                    event.target.value = selection;
                    break;

                case "experienceField":
                    var listExperience =  document.querySelector("select[name='experience']");
                    if(event.target.value == "true"){
                        listExperience.disabled = false;
                    }
                    else{
                        listExperience.disabled = true;
                        listExperience.value = "";
                    }
                    break;
                    
                case "parseField":
                    var parserForm = document.forms[0];
                    var fieldKey = event.target.dataset.name;
                    parserForm[fieldKey].value = selection;
                    break;
                 
            }
        };
        document.addEventListener("click",handlerClick);
  
        //var text = document.querySelector("textarea");
        //text.addEventListener("click", handlerSelect);
        //document.addEventListener("selectend", function(event) {
        //    alert(event.toString());
        //});
        //console.log(window.getSelection().toString())