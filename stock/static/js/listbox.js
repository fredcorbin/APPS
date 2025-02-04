class ListBox{
    constructor(nom,varname) {
        this.properties =  {"writing-mode":"vertical-lr"} ;
        this.varname=varname;
        this.nom=nom;
        this.nRow=0;
        this.selected=-1;
        this.data="";
        this.base=  document.getElementById(nom);
        this.base.style["overflow"]="scroll";
        this.base.addEventListener('click', this.select.bind(null,this.varname));
        }

    select(...args) {
        const elem = args[1].srcElement.id;
        var moi = window[args[0]];
        let id = parseInt(elem.replace(moi.nom,"")) ;
        moi.setSelect(id);
     }

    setSelect(row) {
        let old=this.selected;
        if (old!=row)
        {
            this.selected=row;
            const elemNew= document.getElementById(`${this.nom}${row}`);
            const bk = elemNew.style["background-color"];
            const fg = elemNew.style["color"];
            if (old>-1) {
                const elemOld= document.getElementById(`${this.nom}${old}`);
                elemOld.style["background-color"] = bk;
                elemOld.style["color"]=fg;
                }
            elemNew.style["background-color"] = "darkGrey";
            elemNew.style["color"]="red";

            let value= this.data[row];
            let evt = new CustomEvent('onSelect');
            evt.state={"var":this.varname,"row":this.selected, "id":value.id, "nom" :value.nom , "pref":value.pref};
            if (this.varname=='liste2') console.log(evt.state.row,evt.state.id,evt.state.pref);

            window.dispatchEvent(evt);
        }
    }

    reset() {
        while (this.base.firstChild) { this.base.removeChild(this.base.lastChild);  }
        this.selected=-1;
        let evt = new CustomEvent('onClear');
        evt.state={"var":this.varname};
        window.dispatchEvent(evt);
        }

   newItem(x,nom) {
      let elem=  document.createElement("button");
       elem.style["width"]="100%";
       elem.id=this.nom+x;
       elem.className="w3-bar-item w3-button w3-left-align";
       elem.innerHTML=nom;
       this.base.append(elem);
       return elem;
   }

   setData(data) {
       this.data=data;
       this.nRow= data.length;
       this.reset();
       for (let i=0;i<this.nRow;i++) {
            this.newItem(i,data[i]["nom"]);
            }
       if (this.nRow>0) this.setSelect(0);
   }
}