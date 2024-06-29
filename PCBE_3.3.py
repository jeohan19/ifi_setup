from multiprocessing import Value
from shlex import join
import time
from turtle import *
import turtle
from copy import deepcopy as cp
import os
def bool_checker(object,value=False,type=bool):
    if isinstance(object,type) and object==value:
        return True
    else:
        return False
class Main():
    def __init__(self):
        self.__values={}
        self.__colors={"zelena":"green","bila":"white","oranzova":"orange","fialova":"purple","cerna":"black","modra":"blue","cervena":"red","zluta":"yelow"}
        self.line_num=0
    def __setattr__(self, name, value):
        if name=="raw_text":
            if value=="konec" or value=="chcipni" or value=="zemri" or "vlasi" in value:
                quit()
            super().__setattr__("text",value.split(" "))
        if name=="text":
            try:
                super().__setattr__("raw_text"," ".join(value))
            except:
                stop=False
                a=""
                for i in value:
                    try:
                        a=a+str(i)
                    except:
                        for y in i:
                            a=a+str(y)
                super().__setattr__("raw_text",a)
        super().__setattr__(name,value)
    def __call__(self):
        #print("toto je vstupní věta:",self.text)
        if self.text[0]=="vytvor":
            return self.vytvor()
        elif self.text[0]=="vypis":
            return self.vypis()
        elif self.text[0]=="opakuj":
            opakuj=1
            ted=0
            b=[self.text]
            while opakuj>ted:
                print("co mám opakovat?(zrušíš pomocí 'konec', spustíš pomocí 'ted')")
                a=input("opakuj>>uzivatel>> ").split(" ")
                b.append(a)
                if a[0]=="opakuj":
                    opakuj+=1
                elif a[0]=="ted":
                    ted+=1
                elif a[0]=="konec":
                    return True
            self.line_num=0
            self.repeat_lines=b
            return self.opakuj()
        elif self.text[0]=="kresli":
            return self.kresli()
        elif self.text[0]=="importuj" or self.text[0]=="import":
            return self.importuj()
        elif self.text[0]=="input":
            return self.code_in()
        else:
            return "nevím, co chceš dělat"
    def importuj(self):
        if len(self.text)<2:
            return "zadej argument"
        self.text[1]=" ".join(self.text[1:])
        if not os.path.isfile(self.text[1]):
            try_path=os.path.join(os.getcwd(),self.text[1])
            if not os.path.isfile(try_path):
                print(self.text[1])
                return "soubor nenalezen"
            else:
                self.text[0]=try_path
        lines=[]
        with open(self.text[1],"r",encoding="utf-8") as f:
            for line in f.readlines():
                lines.append(line.replace("\n",""))
        file=self.text[1]
        line_num=0
        while line_num<len(lines):
            if lines[line_num].split(" ")[0]=="opakuj":
                opakuj=1
                ted=0
                old_line=line_num
                b=[lines[line_num].split(" ")]
                line_num+=1
                while opakuj>ted:
                    if line_num>=len(lines):
                        return f"soubor řádek {old_line+1}: neexistuje ukončení opakování"
                    a=lines[line_num].split(" ")
                    
                    
                    if a[0]=="opakuj":
                        opakuj+=1
                    elif a[0]=="ted":
                        ted+=1
                    
                    elif a[0]=="konec":
                        return True
                    if not a[0]=="":
                        b.append(a)
                    line_num+=1
                self.repeat_lines=cp(b)
                result=self.opakuj()
                self.line_num=0
                if not bool_checker(result,True):
                    return f"soubor: opakování na řádku {old_line+1}: {result}"
            elif lines[line_num].split(" ")[0]=="":
                pass
            else:
                self.raw_text=lines[line_num]
                result=self()
                if not bool_checker(result,True):
                    return f"soubor: řádek {line_num+1} ({self.raw_text}) : {result}"
                line_num+=1
        return True
    def vytvor(self):
        try:
            if len(self.text)<3:
                return "vytvor: chybí název proměnné, nebo její obsah"
            self.text[2]=" ".join(self.text[2:])
            try:
                self.text[2]=float(self.text[2])
            except:
                pass
            self.__values[self.text[1]]=self.text[2]
            return True
        except:
            return "vytvor: máš tam někde chybu"
    def vypis(self):
        try: 
            print(self.__values[self.text[1]])
            return True
        except:
            print(" ".join(self.text[1:]))
            return True
    def opakuj(self):
        if len(self.repeat_lines[0])<2:
            self.text.append(input("opakuj>>kolikrát?>>uzivatel>>"))
        times=self.value(self.repeat_lines[0][1],int)
        if bool_checker(times):
            return "neplatný název proměnné, nebo hodnota"
        self.line_num+=1
        line=self.line_num
        for _ in range(times):
            self.line_num=line
            while True:
                #print(self.repeat_lines[self.line_num])
                if self.repeat_lines[self.line_num][0]=="ted":
                    break
                elif self.repeat_lines[self.line_num][0]=="opakuj":
                    result=self.opakuj()
                    if not bool_checker(result,True):
                        return f"opakuj, řádek {self.line_num}: {result}"
                else:
                    self.text=cp(self.repeat_lines[self.line_num])
                    result=self()
                    if not bool_checker(result,True):
                        return f"opakuj: řádek {self.line_num} ({self.raw_text}): {result}"
                self.line_num+=1
        return True
    def kresli(self):
        if self.text[1]=="dopredu" or self.text[1]=="vpred" or self.text[1]=="rovne":
            if len(self.text)<3:
                self.text.append(input("kresli<< vpred <<jak daleko?<< uzivatel<< "))
            return self.turtle_controller(function="forward",value=self.text[2])
        elif self.text[1]=="vlevo" or self.text[1]=="doleva":
            if len(self.text)<3:
                self.text.append("90")
            return self.turtle_controller("left")
        elif self.text[1]=="vpravo" or self.text[1]=="doprava":
            if len(self.text)<3:
                self.text.append("90")
            return self.turtle_controller("right")
        elif self.text[1]=="zvedni" or self.text[1]=="nahoru":
            penup()
            return True
        elif self.text[1]=="dolu" or self.text[1]=="poloz":
            pendown()
            return True
        elif self.text[1]=="zacatek" or self.text[1]=="start":
            home()
            return True
               
        elif self.text[1]=="nastav" or self.text[1]=="presun" or self.text[1]=="bez_na" or self.text[1]=="bez" or self.text[1]=="jed_na" or self.text[1]=="jed":
            raw_values=self.text[2].replace(" ","").split(",")
            if len(raw_values)!=2:
                return "kresli: španý počet argumentů, nebo špatná syntaxe"
            values=[]
            for val in raw_values:
                result=self.value(value=val)
                if isinstance(result,bool) and result==False:
                    return "kresli: špatná hodnota, nebo obsah požadované proměnné"
                else:
                    values.append(result)
            else:
                try:
                    goto(values[0],values[1])
                except:
                    return "kresli: musíš použít absolutní hodnoty"
            return True
        elif self.text[1]=="napis":
            return self.napis() 
        elif self.text[1]=="tvar":
            if self.text[2]=="kruh":
                if len(self.text)<4:
                    self.text.append(input("kresli>>tvar>>kruh>>nenapsal jsi atributy kruhu>>"))
                self.text[3]=self.text[3].split(",")
                result=self.value(value=self.text[3][0])
                if bool_checker(result):
                    return "kresli: špatný atribut průměru"
                self.text[3][0]=result
                attributes={"radius":int(self.text[3][0]),"excent":360,"steps":25}
                for attribute in self.text[3][1:]:
                    attribute=attribute.split(":")
                    if attribute[0]=="kroky" or attribute[0]=="presnost":
                        result=self.value(attribute[1],int)
                        if bool_checker(result):
                            continue
                        else:
                            attributes["steps"]=result
                    elif attribute[0]=="stupne" or attribute[0]=="uhel":
                        result=self.value(attribute[1])
                        if bool_checker(result):
                            continue
                        else:
                            attributes["excent"]=result
                circle(attributes["radius"],attributes["excent"],attributes["steps"])
                return True

            elif self.text[2]=="tecka":
                dot()
                if len(self.text)<4:
                    dot()
                    return True
                result=self.value(self.text[3])
                if bool_checker(result):
                    return "kresli: nepodporovaná hondota nebo proměnná průměru"
                dot(self.text[3],"black")
                return True
            else:
                return "kresli: tvar nenalezen"
        elif self.text[1]=="vypis" or self.text[1]=="pozice":
            print(pos())
            return True
        elif self.text[1]=="zpet":
            undo()
            return True
        elif self.text[1]=="rychlost":
            if len(self.text)<3:
                self.text.append(input("kresli>>rychlost>>jak mám být rychlý?>>"))
            if self.text[2]=="vypis":
                print(speed())
                return True
            result=self.value(ftype=float)
            if bool_checker(result):
                return "kresli: neplatná hodnota, nebo obsah proměné"
            if not(result>0 and result<=10):
                return "kresli: podporována jsou čísla větší, než 0 a menší než 10"
            speed(result)
            return True
        elif self.text[1]=="barva":
            if len(self.text)<3:
                self.text.append(input("kresli>>barva>>jaká?>>"))
            result=self.color(self.text[2])
            if bool_checker(result):
                return "kresli: neplatná barva"
            try:
                color(result)
            except Exception as e:
                try:
                    yi=[]
                    for i in result:
                        yi.append(int(i))
                    print(tuple(yi))
                    fillcolor(tuple(yi))
                except Exception as ee:
                    return f"kresli: neplatný druh barvy: \n{e} \n \n {ee}"
            return True
        elif self.text[1]=="resetuj" or self.text[1]=="vycisti":
            clearscreen()
            return True
        else:
            return "kresli: nevím, co mám dělat"
    def napis(self):
        if len(self.text)<3:
            self.text.append(input("kresli>>co?>>"))
        self.text[2]=" ".join(self.text[2:])
        if self.text[2] in self.__values:
            write(self.__values[self.text[2]],font=("Arial",30,"normal"))
        else:
            write(self.text[2],font=("Arial",30,"normal"))
        return True
    def code_in(self):
        if len(self.text)<2:
            self.text.append(input("opakuj<<do jaké proměné?<<uzivatel<< "))
        if len(self.text)>2:
            self.__values[self.text[1]]=input(" ".join(self.text[2:])+"<< ")
        else:
            self.__values[self.text[1]]=input(f"input z kódu({self.text[1]})<<uzivatel<< ")
        return True
    def value(self,value=None,ftype=float):
        if value==None:
            value=self.text[2]
        try:

            value=ftype(value)
            return value
        except:
            try:
                value=ftype(self.__values[value])
                return value
            except:
                return False
    def turtle_controller(self,function,value=None):
        # old, don't use in complicated functions
        if value==None:
            value=self.text[2]


        result=self.value(value)
        if bool_checker(result):
            return "kresli: špatná hodnota nebo obsah proměnné"
        exec(function+"(result)")
        return True
    def color(self,x):
        result = self.value(value=x,ftype=str)
        if result in self.__colors:
            return self.__colors[result]
        else:
            try:
                x=x.split(",")
                if len(x)!=3:
                    return False
            except:
                return False
            z=[]
            for y in x:
                result=self.value(y)
                if bool_checker(result):
                    return False
                z.append(result)
            return tuple(z)
main=Main()
while True:
    main.raw_text=input("uzivatel>> ").replace("  "," ")
    result=main()
    if result!=True:
        print("chyba<<",result)
