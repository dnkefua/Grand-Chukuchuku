import json
E=json.load(open('/tmp/ed/edl5.json')); D=json.load(open('/tmp/ed/vo/durs_t.json'))
EN={'L01':["Today is the day. No retreat, no surrender, Zino?","Once a goal goes in, no refund!"],
'L02':["My 100 francs has ambition. Big ambition.","Six of us have put in. The winning team takes 600,","200 for each man. Three goals. My blood is hot."],
'L03':["Talk all you want, Zino.","Today your knee will kiss the gravel."],
'L04':["Hey! It's only a game. No need for war."],
'L05':["Pass it! There's space at the back post!"],
'L06':["Zino, the back post is open!"],
'L07':["I've got him covered. Go in!"],
'L08':["They can't catch me!"],
'L10':["Sorry, Ayuk. Get up."],
'L11':["ONE-nil!"],
'L12':["Arey one, Zino zero!","Zino, your bottle is crying!"],
'L13':["Ayuk, one touch! Robi, cover!"],
'L14':["Wait! Where did the pass go?!"],
'L15':["Chai!"],
'L16':["Did you come to play ball","or to scrape my skin?!"],
'L17':["That was the gravel testing you, not me!"],
'L18a':["GOAL! Equalizer!"],
'L18b':["One-one!"],
'L19':["That's it!"],
'L20':["Two-two!","Next goal takes the 600!"],
'L21':["GOAL! THREE! The bottle rang like a church bell!","Bring the 600!"],
'L22':["What goal?! It didn't touch!","A foot pushed the bottle. That one doesn't count!"],
'L23':["That's a clean goal."],
'L24':["It's only 200 francs. No need to fight!"],
'L25':["Get out of the way, Pastor!"],
'L26':["When a man passes you, you carry his bag."],
'L27':["What is this?"],
'L28':["It's old man style.","Your own force comes back to you."],
'L29':["Kung fu will finish you all!"],
'L30':["You're all blowing wind, not fire."],
'L31':["Bruce Lee meets Grandpa on Fiango road!"],
'L32':["ENOUGH!"],
'L33':["You're fighting over 600 francs on the road?","I saw the match,","and little bro Zino's team won."],
'L34':["Grand Nestor, the ball didn't touch the bottle!"],
'L35':["Don't worry. Next match."],
'L36':["Take your money. And Arey, football is not a fight.","Go and clean your mouth."],
'L37':["Yes, Grand Nestor."],
'L38':["Thank you, Grand. Two hundred for Ayuk,","two hundred for Robi, two hundred for me."],
'L39':["Chai! A champion with a bloody knee!"]}
FR={'L01':["C'est aujourd'hui le jour. Pas de retraite, pas de reddition, Zino ?","Une fois le but marqué, pas de remboursement !"],
'L02':["Mes 100 francs ont de l'ambition. Une grande ambition.","On a misé à six. L'équipe gagnante empoche 600,","200 chacun. Trois buts. J'ai le sang chaud."],
'L03':["Parle autant que tu veux, Zino.","Aujourd'hui ton genou va embrasser le gravier."],
'L04':["Eh ! Ce n'est qu'un jeu. Pas besoin de guerre."],
'L05':["Passe ! Il y a de l'espace au deuxième poteau !"],
'L06':["Zino, le deuxième poteau est ouvert !"],
'L07':["Je le couvre. Entre !"],
'L08':["Ils ne peuvent pas m'attraper !"],
'L10':["Désolé, Ayuk. Lève-toi."],
'L11':["UN-zéro !"],
'L12':["Arey un, Zino zéro !","Zino, ta bouteille pleure !"],
'L13':["Ayuk, une touche ! Robi, couvre !"],
'L14':["Attends ! Où est passée la passe ?!"],
'L15':["Chai !"],
'L16':["Tu es venu jouer au ballon","ou m'arracher la peau ?!"],
'L17':["C'est le gravier qui t'a goûté, pas moi !"],
'L18a':["BUT ! Égalisation !"],
'L18b':["Un partout !"],
'L19':["C'est ça !"],
'L20':["Deux partout !","Le prochain but rafle les 600 !"],
'L21':["BUT ! TROIS ! La bouteille a sonné comme une cloche d'église !","Amenez les 600 !"],
'L22':["Quel but ?! Ça n'a pas touché !","C'est un pied qui a poussé la bouteille. Celui-là ne compte pas !"],
'L23':["C'est un but propre."],
'L24':["Ce n'est que 200 francs. Pas besoin de se battre !"],
'L25':["Dégage de la route, Pasteur !"],
'L26':["Quand un homme te dépasse, tu portes son sac."],
'L27':["C'est quoi, ça ?"],
'L28':["C'est le style des anciens.","Ta propre force te revient."],
'L29':["Le kung-fu va vous finir !"],
'L30':["Vous soufflez du vent, pas du feu."],
'L31':["Bruce Lee rencontre Grand-père sur la route de Fiango !"],
'L32':["ÇA SUFFIT !"],
'L33':["Vous vous battez pour 600 francs sur la route ?","J'ai vu le match,","et c'est l'équipe du petit frère Zino qui a gagné."],
'L34':["Grand Nestor, le ballon n'a pas touché la bouteille !"],
'L35':["Ne t'inquiète pas. Au prochain match."],
'L36':["Prends ton argent. Et Arey, le football n'est pas une bagarre.","Va te laver la bouche."],
'L37':["Oui, Grand Nestor."],
'L38':["Merci, Grand. Deux cents pour Ayuk,","deux cents pour Robi, deux cents pour moi."],
'L39':["Chai ! Un champion avec un genou en sang !"]}
def ts(t):
    h=int(t//3600); m=int(t%3600//60); s=t%60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}".replace(',1000',',999')
cues=[]
for it in E:
    for lid,off in it['lines']:
        if lid not in EN: continue
        t0=it['start']+off; dur=D[lid]; parts=EN[lid]
        w=[len(p) for p in parts]; tot=sum(w); a=t0
        for i,p in enumerate(parts):
            b=a+dur*w[i]/tot
            cues.append((a,max(b,a+0.8),lid,i))
            a=b
cues.sort()
for lang,TX in (('en',EN),('fr',FR)):
    out=[]
    for n,(a,b,lid,i) in enumerate(cues):
        nb=cues[n+1][0]-0.05 if n+1<len(cues) else b
        b=min(b+0.3,max(nb,a+0.8))
        out.append(f"{n+1}\n{ts(a)} --> {ts(b)}\n{TX[lid][i]}\n")
    open(f'/tmp/ed/ep07.{lang}.srt','w',encoding='utf-8').write('\n'.join(out))
print(len(cues))
