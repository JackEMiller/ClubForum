from main import app
from flask import Flask, render_template, request, session, redirect, url_for
from init_app import Users, Classes, ClassesMember, ClassesTechnique, Techniques, Members, db


@app.route('/viewclass/<int:id>', methods=['GET','POST'])
def viewclass(id):
    class_ = Classes.query.get(id)
    techniques = ClassesTechnique.filter_by(class_id = id).all()
    members = ClassesMember.filter_by(class_id = id).all()
    techniques_list = []
    members_list = []
    for technique in techniques:
        techniques_list.append(Techniques.filter_by(id = technique.technique_id).first())
    for member in members:
        members_list.append(Techniques.filter_by(id = member.member_id).first())
    return render_template('viewclass.html',currentclass = class_, members = members, techniques = techniques)


@app.route('/deleteclass/<int:cid>')
def deleteclass(cid):
    item = Classes.query.get(cid)

    return redirect('/view/0')


@app.route('/updatetransaction/<int:cid>/<int:tid>', methods=['GET','POST'])
def updatetransaction(cid,tid):
    item = Classes.query.get(cid)
    if request.method == 'POST':
        c_id = request.form['customer']
        pid = request.form['product']
        c_id = c_id.split()
        pid = pid.split()
        item.customer_id = c_id[0]
        item.product_id = pid[0]
        db.session.add(item)
        db.session.commit()
        return redirect('/viewtransaction/'+str(cid))
    else:
        customers_id = []
        customers = Members.query.all()
        for customer in customers:
            customers_id.append(str(customer.id) + " " + customer.first_name)
        products_id = []
        products = Techniques.query.all()
        for product in products:
            products_id.append(str(product.id) + " " + product.name)
        return render_template('updatetransaction.html',customers = customers_id,products = products_id)


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


@app.route('/view/<int:error>')
def view(error):
    errortext = ""
    if error == 1:
        errortext = "Can't delete customer that has transactions, please delete transactions first"
    if error == 2:
        errortext = "Can't delete product that has transactions, please delete transactions first"
    members = Members.query.all()
    techniques = Techniques.query.all()
    return render_template('view.html',customers=members, products=techniques, errortext=errortext)


@app.route('/deletemember/<int:id>')
def deletemember(id):
    if ClassesMember.query.filter_by(customer_id = id).first() is not None:
        return redirect('/view/1')
    else:
        item = Members.query.get(id)
        db.session.delete(item)
        db.session.commit()
        return redirect('/view/0')


@app.route('/updatemember/<int:id>', methods=['GET','POST'])
def updatemember(id):
    item = Members.query.get(id)
    if request.method == 'POST':
        texta = request.form['name']
        textb = request.form['level']
        textc = request.form['affiliation']
        item.name = texta
        item.level = textb
        item.affiliation = textc
        db.session.commit()
        return redirect('/view/0')
    return render_template('updatemember.html', customer=item)


@app.route('/updatetechnique/<int:id>', methods=['GET','POST'])
def updatetechnique(id):
    item = Techniques.query.get(id)
    if request.method == 'POST':
        texta = request.form['name']
        textb = request.form['difficulty']
        textc = request.form['description']
        item.name = texta
        item.difficulty = textb
        item.description = textc
        db.session.commit()
        return redirect('/view/0')
    return render_template('updatetechnique.html', product=item)


@app.route('/deletetechnique/<int:id>')
def deletetechnique(id):
    if Techniques.query.filter_by(product_id = id).first() is not None:
        return redirect('/view/2')
    else:
        item = Techniques.query.get(id)
        db.session.delete(item)
        db.session.commit()
        return redirect('/view/0')


@app.route('/view/<int:error>', methods=['POST'])
def view_post(error):
    str = request.form['submitbutton']
    if str == "product":
        texta = request.form['name']
        textb = request.form['price']
        new_product = Techniques(name=texta, price=textb)
        db.session.add(new_product)
        db.session.commit()
    if str == "customer":
        texta = request.form['fname']
        textb = request.form['sname']
        new_customer = Members(first_name=texta, last_name=textb)
        db.session.add(new_customer)
        db.session.commit()
    if str == "transaction":
        cid = request.form['customer']
        pid = request.form['product']
        cid = cid.split()
        pid = pid.split()
        new_transaction = Classes(customer_id=cid[0], product_id=pid[0])
        db.session.add(new_transaction)
        db.session.commit()
    return redirect('/view/0')