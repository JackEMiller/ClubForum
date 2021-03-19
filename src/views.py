from flask import Flask, render_template, request, session, redirect, url_for, blueprints
try:
    from src.models import Users, Classes, ClassesMember, ClassesTechnique, Techniques, Members, db
except:
    from models import Users, Classes, ClassesMember, ClassesTechnique, Techniques, Members, db

app = blueprints.Blueprint('app',__name__,static_folder='templates')

# tested
@app.route('/viewclass/<int:typeof>/<int:id>', methods=['GET','POST'])
def viewclass(typeof,id):
    classes_ = None
    printarray = []
    if typeof == 0:
        classes_ = Classes.query.all()
    if typeof == 1:
        classes_ = ClassesMember.query.filter_by(member_id = id).all()
    if typeof == 2:
        classes_ = ClassesTechnique.query.filter_by(technique_id = id).all()
    for class_ in classes_:
        techs = []
        membs = []
        techniques = ClassesTechnique.query.filter_by(class_id=class_.id).all()
        members = ClassesMember.query.filter_by(class_id=class_.id).all()
        for technique in techniques:
            a = Techniques.query.filter_by(id = technique.technique_id).first()
            if a is not None:
                techs.append([a.name,a.difficulty,a.description])
        for member in members:
            a = Members.query.filter_by(id = member.member_id).first()
            if a is not None:
                membs.append([a.name,a.level,a.affiliation])
        printarray.append([class_,techs,membs])
    return render_template('viewclass.html', classarray=printarray)

# tested
@app.route('/deleteclass/<int:cid>')
def deleteclass(cid):
    item = Classes.query.filter_by(id=cid).first()
    techniques = ClassesTechnique.query.filter_by(class_id=cid)
    members = ClassesMember.query.filter_by(class_id=cid)
    for technique in techniques:
        db.session.delete(technique)
    for member in members:
        db.session.delete(member)
    db.session.commit()
    db.session.delete(item)
    db.session.commit()
    return redirect('/viewclass/0/0')

# tested
@app.route('/addupdatemember/<int:cid>')
def addupdatemember(cid):
    member = Members.query.first()
    newmemclass = ClassesMember(class_id=cid,member_id=member.id)
    db.session.add(newmemclass)
    db.session.commit()
    return redirect('/updateclass/'+str(cid))

# tested
@app.route('/addupdatetechnique/<int:cid>')
def addupdatetechnique(cid):
    technique = Techniques.query.first()
    newtechclass = ClassesTechnique(class_id=cid,technique_id=technique.id)
    db.session.add(newtechclass)
    db.session.commit()
    return redirect('/updateclass/'+str(cid))

# tested
@app.route('/deleteupdatetechnique/<int:cid>')
def deleteupdatetechnique(cid):
    item = ClassesTechnique.query.filter_by(class_id = cid).first()
    db.session.delete(item)
    db.session.commit()
    return redirect('/updateclass/'+str(cid))

# tested
@app.route('/deleteupdatemember/<int:cid>')
def deleteupdatemember(cid):
    item = ClassesMember.query.filter_by(class_id = cid).first()
    db.session.delete(item)
    db.session.commit()
    return redirect('/updateclass/'+str(cid))

# tested
@app.route('/updateclass/<int:cid>', methods=['GET','POST'])
def updateclass(cid):
    if request.method == 'GET':
        item = Classes.query.filter_by(id=cid).first()
        alltechniques = Techniques.query.all()
        allmembers= Members.query.all()
        currenttechniques = ClassesTechnique.query.filter_by(class_id = cid).all()
        currentmembers = ClassesMember.query.filter_by(class_id=cid).all()
        return render_template('updateclass.html', currentclass=item, techniques=alltechniques, members=allmembers,
                               currentmembers=currentmembers,currenttechniques=currenttechniques)
    if request.method == 'POST':
        item = Classes.query.filter_by(id=cid).first()
        techniques = ClassesTechnique.query.filter_by(class_id=cid).all()
        members = ClassesMember.query.filter_by(class_id=cid).all()
        for tech in techniques:
            db.session.delete(tech)
        for mem in members:
            db.session.delete(mem)
        db.session.commit()
        item.date = request.form['classdate']
        for mem in members:
            memberid = request.form[str(mem.id)]
            newinteresct = ClassesMember(class_id = cid, member_id = memberid)
            db.session.add(newinteresct)
            db.session.commit()
        for tech in techniques:
            techniqueid = request.form[str(tech.id)]
            newinteresct = ClassesTechnique(class_id = cid, technique_id = techniqueid)
            db.session.add(newinteresct)
            db.session.commit()
        return redirect('/viewclass/0/0')

# tested
@app.route('/signup', methods=['GET','POST'])
def signup():
    errortext = ""
    if request.method == 'POST':
        texta = request.form['Username']
        textb = request.form['Password']
        if texta == "":
            errortext = "No username inserted"
            return render_template('signup.html', errortext=errortext)
        if textb == "":
            errortext = "No password inserted"
            return render_template('signup.html', errortext=errortext)
        if Users.query.get(texta) is not None:
            errortext = "Username already exists please choose a different name"
            render_template('signup.html', errortext=errortext)
        else:
            new_user = Users(user_name=texta, password=textb)
            db.session.add(new_user)
            db.session.commit()
            errortext = "success"
            return render_template('signup.html', errortext=errortext)
    return render_template('signup.html')

# tested
@app.route('/', methods=['GET','POST'])
def index():
    errortext = ""
    if request.method == 'POST':
        texta = request.form['Username']
        textb = request.form['Password']
        if texta == "":
            errortext = "No username inserted"
            return render_template('index.html', errortext=errortext)
        if textb == "":
            errortext = "No password inserted"
            return render_template('index.html', errortext=errortext)
        if errortext == "":
            user = Users.query.get(texta)
            if user is not None:
                if textb == user.password:
                    return redirect('/view/0')
    else:
        return render_template('index.html')

# tested
@app.route('/view/<int:error>')
def view(error):
    errortext = ""
    if error == 1:
        errortext = "Can't delete "
    if error == 2:
        errortext = "Can't delete "
    members = Members.query.all()
    techniques = Techniques.query.all()
    return render_template('view.html',members=members, techniques=techniques, errortext=errortext)

# tested
@app.route('/deletemember/<int:id>')
def deletemember(id):
    if ClassesMember.query.filter_by(member_id = id).first() is not None:
        return redirect('/view/1')
    else:
        item = Members.query.filter_by(id=id).first()
        db.session.delete(item)
        db.session.commit()
        return redirect('/view/0')

# tested
@app.route('/updatemember/<int:id>', methods=['GET','POST'])
def updatemember(id):
    item = Members.query.filter_by(id=id).first()
    if request.method == 'POST':
        texta = request.form['name']
        textb = request.form['level']
        textc = request.form['affiliation']
        item.name = texta
        item.level = textb
        item.affiliation = textc
        db.session.commit()
        return redirect('/view/0')
    return render_template('updatemember.html', member=item)

# tested
@app.route('/updatetechnique/<int:id>', methods=['GET','POST'])
def updatetechnique(id):
    item = Techniques.query.filter_by(id=id).first()
    if request.method == 'POST':
        texta = request.form['name']
        textb = request.form['difficulty']
        textc = request.form['description']
        item.name = texta
        item.difficulty = textb
        item.description = textc
        db.session.commit()
        return redirect('/view/0')
    return render_template('updatetechnique.html', technique=item)

# tested
@app.route('/deletetechnique/<int:id>')
def deletetechnique(id):
    if ClassesTechnique.query.filter_by(technique_id = id).first() is not None:
        return redirect('/view/2')
    else:
        item = Techniques.query.filter_by(id = id).first()
        db.session.delete(item)
        db.session.commit()
        return redirect('/view/0')

# tested
@app.route('/addclass/<int:studentcount>/<int:techniquecount>', methods=['POST','GET'])
def addclass(studentcount,techniquecount):
    sarray = []
    tarray = []
    for i in range(1,studentcount+1):
        sarray.append(i)
    for i in range(1, techniquecount+1):
        tarray.append(i)
    techs = Techniques.query.all()
    membs = Members.query.all()
    if request.method == 'POST':
        classdate = request.form['classdate']
        newclass = Classes(date=classdate)
        db.session.add(newclass)
        db.session.commit()
        for i in range(1, studentcount + 1):
            membername = request.form[str(i)]
            newinteresct = ClassesMember(class_id = newclass.id, member_id = Members.query.
                                         filter_by(name=membername).first().id)
            db.session.add(newinteresct)
            db.session.commit()
        for i in range(1, techniquecount + 1):
            techniquename = request.form[str(i)+"a"]
            newinteresct = ClassesTechnique(class_id = newclass.id, technique_id = Techniques.query.
                                            filter_by(name=techniquename).first().id)
            db.session.add(newinteresct)
            db.session.commit()
        return redirect('/viewclass/0/0')
    return render_template('addclass.html', studentcount=sarray,techniquecount=tarray,techniques=techs,
                           students=membs)

# tested
@app.route('/view/<int:error>', methods=['POST'])
def view_post(error):
    str = request.form['submitbutton']
    if str == "technique":
        texta = request.form['name']
        textb = request.form['difficulty']
        textc = request.form['description']
        new_technique = Techniques(name=texta, difficulty=textb, description=textc)
        db.session.add(new_technique)
        db.session.commit()
    if str == "member":
        texta = request.form['name']
        textb = request.form['level']
        textc = request.form['affiliation']
        new_member = Members(name=texta, level=textb, affiliation=textc)
        db.session.add(new_member)
        db.session.commit()
    if str == "addclass":
        texta = request.form['studentscount']
        textb = request.form['techniquescount']
        return redirect('/addclass/'+texta+'/'+textb)
    return redirect('/view/0')