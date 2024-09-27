opt_array_wasteWater = [
    { text: 'Cleaning ink - Press 1', value: 'Cleaning ink Press1' } ,
    { text: 'Cleaning ink - Press 2', value: 'Cleaning ink Press2' } ,
    { text: 'Plate Processing', value: 'Plate Processing' } ,
    { text: 'Fountain Solution - Press1', value: 'Fountain Solution Press1' },
    { text: 'Fountain Solution - Press2', value: 'Fountain Solution Press2' }
];

opt_array_wastePaper = [
    { text: 'Flaky Waste Paper', value: 'Flaky Waste Paper' } ,
    { text: 'Pieces Waste Paper - Cutting Machine 1', value: 'Pieces Waste Paper Cutting Machine 1' } ,
    { text: 'Pieces Waste Paper - Cutting Machine 2', value: 'Pieces Waste Paper Cutting Machine 2' } ,
    { text: 'Pieces Waste Paper - 3-sided trimmer', value: 'Pieces Waste Paper Cutting 3-sided trimmer' } ,
    { text: 'Sheet Waste Paper - Press 1', value: 'Sheet Waste Paper Press 1' } ,
    { text: 'Sheet Waste Paper - Press 2', value: 'Sheet Waste Paper Press 2' } ,
    { text: 'Sheet Waste Paper - Press 3', value: 'Sheet Waste Paper Press 3' } ,
    { text: 'Sheet Waste Paper - Press 4', value: 'Sheet Waste Paper Press 4' } ,
];
//	選択リストを作る関数 
//
function chgPulldown(obj){
    // リセット
    obj.selector.disabled = false;
    
    var radioSelectList = document.getElementsByName("radio");
    var radioSelect="";
    for(var i=0; i<radioSelectList.length; i++){
        if (radioSelectList[i].checked) {
            radioSelect = radioSelectList[i].value;
            break;
        };
    }
    if(radioSelect == "wasteWater"){
        createSelection(obj, opt_array_wasteWater);
    } else if(radioSelect == "wastePaper"){
        createSelection(obj, opt_array_wastePaper);
    } 
    
}
//	選択リストを作る関数 
//	引数: ( selectオブジェクト, option配列  )
//
function createSelection( obj, opt_array ){
    var doc = obj.selector;
    doc.length = 0;
    
    // 整形
    for( var i=0; i < opt_array.length; i++){
        doc.length++;
        doc.options[ doc.length - 1].value = opt_array[i].value;
        doc.options[ doc.length - 1].text  = opt_array[i].text;
    };
}

document.addEventListener('DOMContentLoaded', () => {
    const dateField = document.getElementById('date');
    const today = new Date().toISOString().split('T')[0];
    dateField.value = today;
});