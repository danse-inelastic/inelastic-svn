#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                               Orthologue, Ltd.
#                      (C) 2004-2006  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component


class Scribe(Component):


    def renderExpenses(self, director, actor, routine, document, expenses,
                       editable=True, selectable=False, sortable=False):
        sentry = director.sentry

        # if none, say and return
        if not expenses:
            p = document.paragraph()
            p.text = [
                "You do not have any outstanding expenses"
                ]
            return

        # prepare the table header links that set the sort order
        if sortable:
            actions = [
                "actor=%s" % actor,
                "routine=%s" % routine,
                "sentry.username=%s" % sentry.username,
                "sentry.ticket=%s" % sentry.ticket,
                ]

            amountlink = '<a href="%s?%s">Amount</a>' % (
                director.cgihome, "&".join(actions+["%s.order=amount" % actor]))

            categorylink = '<a href="%s?%s">Category</a>' % (
                director.cgihome, "&".join(actions+["%s.order=category" % actor]))

            codelink = '<a href="%s?%s">Code</a>' % (
                director.cgihome, "&".join(actions+["%s.order=code" % actor]))

            datelink = '<a href="%s?%s">Date</a>' % (
                director.cgihome, "&".join(actions+["%s.order=date" % actor]))
        else:
            amountlink = 'Amount'
            categorylink = 'Category'
            codelink = 'Code'
            datelink = 'Date'

        text = [
            '<p>',
            '<table cellspacing="0" class="expenseTable">',
            '  <thead>',
            '    <tr class="expenseHeader">',
            '      <th>&nbsp;</th>',
            ]

        if selectable:
            text.append(
            '      <th><img src="images/linkOpaque.gif"'
            '          onClick="flipCheckboxes('
            '              document.forms[\'expenseSelection\'].elements[\'expenses\'])'
            '          ">'
            '      </th>'
            )

        text += [
            '      <th>%s</th>' % datelink,
            '      <th>%s</th>' % codelink,
            '      <th>%s</th>' % categorylink,
            '      <th>Description</th>',
            '      <th>%s</th>' % amountlink,
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        total = 0.0
        for index, t in enumerate(expenses):
            # update the total
            total += t.amount

            # compute the row marker
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            if editable:
                actions = [
                    "actor=purser",
                    "routine=edit",
                    "purser.id=%s" % t.id,
                    "sentry.username=%s" % sentry.username,
                    "sentry.ticket=%s" % sentry.ticket,
                    ]
                link = '<a href="%s?%s">%s</a>' % (director.cgihome, "&".join(actions), index+1)
            else:
                link = '%s' % (index+1)

            description = t.description
            if not description:
                description = "&nbsp;"
            code = "&nbsp;".join(t.code.split())
            text += [
                '    <tr class="%s">' % marker,
                '      <td class="expenseIndex">%s</td>' % link,
                ]

            if selectable:
                selector = '<input checked type="checkbox" name="expenses" id="%s">' % (t.id)
                text.append('      <td>%s</td>' % selector)

            text += [
                '      <td class="expenseDate">%s</td>' % t.date,
                '      <td class="expenseCode">%s</td>' % code,
                '      <td class="expenseCategory">%s</td>' % t.category,
                '      <td class="expenseDescription">%s</td>' % description,
                '      <td class="expenseAmount">$%.2f</td>' % t.amount,
                '    </tr>',
                ]

        text += [
            '    <tr class="expenseFooter">',
            '      <td>&nbsp;</td>',
            ]
        if selectable:
            text.append('      <td>&nbsp;</td>')

        text += [
            '      <td class="expenseTotal" colspan=4>',
            '        Total:',
            '      </td>',
            '      <td class="expenseAmount">$%.2f</td>' % total,
            '    </tr>',
            '  </tbody>',
            '</table>',
            '</p>',
            ]

        if not selectable:
            # draw the table and get out
            table = document.literal()
            table.text = text
            return
        
        # expenses are selectable
        # build the form that gathers the expense info
        form = document.form(
            name='expenseSelection', legend="Select expenses", action=director.cgihome,
            onSubmit= (
                'return gatherCheckboxes('
                'this.elements["expenses"], this.elements["%s.expenses"]);' % actor
                )
            )
        targetActor = form.hidden(name="actor", value=actor)
        targetRoutine = form.hidden(name="routine", value="confirmExpenseReport")
        targetReports = form.hidden(name="%s.expenses" % actor, value="")
        user = form.hidden(name="sentry.username", value=sentry.username)
        ticket = form.hidden(name="sentry.ticket", value=sentry.ticket)

        p = form.paragraph()
        p.text = text
        
        # the submit button
        submit = form.control(name="submit", type="submit", value="submit")

        return


    def renderExpenseSummaryByChargeCode(self, director, document, codes, summary):
        table = document.literal()
        text = [
            '<p>',
            '<table cellspacing="0" class="expenseTable">',
            '  <thead>',
            '    <tr class="expenseHeader">',
            '      <th>Code</th>',
            '      <th>Description</th>',
            '      <th>Amount</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        keys = summary.keys()
        keys.sort()

        total = 0.0
        for index, code in enumerate(keys):
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            amount = summary[code]
            total += amount
            description = codes[code].description
            text += [
                '    <tr class="%s">' % marker,
                '      <td class="expenseCode">%s</td>' % code,
                '      <td class="expenseDescription">%s</td>' % description,
                '      <td class="expenseAmount">$%.2f</td>' % amount,
                '    </tr>',
                ]

        text += [
            '    <tr class="expenseFooter">',
            '      <td class="expenseTotal" colspan=2>',
            '        Total:',
            '      </td>',
            '      <td class="expenseAmount">$%.2f</td>' % total,
            '    </tr>',
            '  </tbody>',
            '</table>',
            '</p>',
            ]

        table.text = text

        return


    def renderUserExpenseReports(self, director, document, username, reports, actions=None):
        # if none, say and return
        if not reports:
            p = document.paragraph(cls="error")
            p.text = [
                "No expense reports were selected. Please try again."
                ]
            return

        clerk = director.clerk
        
        # index employees
        employees = clerk.indexEmployees()

        # start building the table
        table = document.literal()
        text = [
            '<p>',
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th>Report</th>',
            ]
        if username == "all employees":
            text.append('      <th>Employee</th>')
        text += [
            '      <th>Submitted</th>',
            '      <th>Amount</th>',
            '      <th>Status</th>',
            '      <th>Paid</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        total = 0.0
        for index, t in enumerate(reports):
            reportTotal = 0.0
            expenses = clerk.retrieveReportedExpenses(t.id)
            fullname = employees[t.employee].fullname
            for expense in expenses:
                reportTotal += expense.amount
            total += reportTotal

            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            if actions:
                target = "&".join(actions) % t.id
                link = '<a href="%s?%s">%s</a>' % (director.cgihome, target, t.id)
            else:
                link = t.id

            paid = "&nbsp;"
            if t.status == 'p':
                reimbursement = clerk.retrieveReportReimbursment(t.id)
                if reimbursement:
                    paid = reimbursement.submitted

            text += [
                '    <tr class="%s">' % marker,
                '      <td class="index">%s</td>' % link,
                ]
            if username == "all employees":
                text.append('      <td class="text">%s</td>' % t.employee)
            text += [
                '      <td class="date">%s</td>' % t.submitted,
                '      <td class="number">$%.2f</td>' % reportTotal,
                '      <td class="status">%s</td>' % t.status,
                '      <td class="date">%s</td>' % paid,
                '    </tr>',
                ]

        if username == "all employees":
            colspan = 2
        else:
            colspan = 1
        text += [
            '    <tr class="footer">',
            '      <td>&nbsp;</td>',
            '      <td class="total" colspan="%d">' % colspan,
            '        Total:',
            '      </td>',
            '      <td class="number">$%.2f</td>' % total,
            '      <td>&nbsp;</td>',
            '      <td>&nbsp;</td>',
            '    </tr>',
            '  </tbody>',
            '</table>',
            '</p>',
            ]

        table.text = text

        return


    def renderTimeCharges(self, director, document, charges, editable=True):
        # if none, say and return
        if not charges:
            p = document.paragraph()
            p.text = [
                "You do not have any outstanding time charges"
                ]
            return

        # else, generate the table
        table = document.literal()
        text = [
            '<p>',
            '<table cellspacing="0" class="timechargeTable">',
            '  <thead>',
            '    <tr class="timechargeHeader">',
            '      <th>&nbsp;</th>',
            '      <th>Date</th>',
            '      <th>Code</th>',
            '      <th>Description</th>',
            '      <th>Duration<br>days</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        total = 0.0
        for index, t in enumerate(charges):
            total += t.duration
            
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            if editable:
                actions = [
                    "actor=timekeeper",
                    "routine=edit",
                    "timekeeper.id=%s" % t.id,
                    "sentry.username=%s" % director.sentry.username,
                    "sentry.ticket=%s" % director.sentry.ticket,
                    ]
                link = '<a href="%s?%s">%s</a>' % (director.cgihome, "&".join(actions), index+1)
            else:
                link = '%s' % (index+1)

            description = t.description
            if not description:
                description = "&nbsp;"
            text += [
                '    <tr class="%s">' % marker,
                '      <td class="timechargeIndex">%s</td>' % link,
                '      <td class="timechargeDate">%s</td>' % t.date,
                '      <td class="timechargeCode">%s</td>' % "&nbsp;".join(t.code.split()),
                '      <td class="timechargeDescription">%s</td>' % description,
                '      <td class="timechargeDuration">%.2f</td>' % t.duration,
                '    </tr>',
                ]

        text += [
            '    <tr class="timechargeFooter">',
            '      <td class="timechargeTotal" colspan=4>',
            '        Total:',
            '      </td>',
            '      <td class="timechargeDuration">%.2f</td>' % total,
            '    </tr>',
            '  </tbody>',
            '</table>',
            '</p>',
            ]

        table.text = text

        return


    def renderTimechargeSummaryByChargeCode(self, director, document, codes, summary):
        table = document.literal()
        text = [
            '<p>',
            '<table cellspacing="0" class="timechargeTable">',
            '  <thead>',
            '    <tr class="timechargeHeader">',
            '      <th>Code</th>',
            '      <th>Description</th>',
            '      <th>Duration<br>(days)</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        keys = summary.keys()
        keys.sort()

        total = 0.0
        for index, code in enumerate(keys):
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            duration = summary[code]
            total += duration
            description = codes[code].description
            text += [
                '    <tr class="%s">' % marker,
                '      <td class="timechargeCode">%s</td>' % code,
                '      <td class="timechargeDescription">%s</td>' % description,
                '      <td class="timechargeDuration">%.2f</td>' % duration,
                '    </tr>',
                ]

        text += [
            '    <tr class="timechargeFooter">',
            '      <td class="timechargeTotal" colspan=2>',
            '        Total:',
            '      </td>',
            '      <td class="timechargeDuration">%.2f</td>' % total,
            '    </tr>',
            '  </tbody>',
            '</table>',
            '</p>',
            ]

        table.text = text

        return


    def renderTimeChargeReports(self, director, document, reports):
        # if none, say and return
        if not reports:
            p = document.paragraph()
            p.text = [
                "You have not submitted any time reports."
                ]
            return

        p = document.paragraph()
        p.text = [
            "The following table lists all the time reports you have submitted.",
            "You can view the associated expense detail by following the link in the",
            "first column of the table."
            ]

        table = document.literal()
        text = [
            '<p>',
            '<table cellspacing="0" class="timechargeTable">',
            '  <thead>',
            '    <tr class="timechargeHeader">',
            '      <th>Report</th>',
            '      <th>Submitted</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        for index, t in enumerate(reports):
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            actions = [
                "actor=timekeeper",
                "routine=viewTimeChargeReport",
                "timekeeper.id=%s" % t.id,
                "sentry.username=%s" % director.sentry.username,
                "sentry.ticket=%s" % director.sentry.ticket,
                ]
            link = '<a href="%s?%s">%s</a>' % (director.cgihome, "&".join(actions), t.id)

            text += [
                '    <tr class="%s">' % marker,
                '      <td class="timechargeIndex">%s</td>' % link,
                '      <td class="timechargeDate">%s</td>' % t.submitted,
                '    </tr>',
                ]

        text += [
            '  </tbody>',
            '</table>',
            '</p>',
            ]

        table.text = text

        return


    def expenseForm(self, actor, context, document, defaults, errors=None, new=True):
        import ent.content
        
        # get access to the app context
        clerk = context.clerk
        sentry = context.sentry

        if errors:
            p = document.paragraph(cls="error")
            p.text = [
                "The form you filled out contained some errors.",
                "Please look through the data you have entered and correct any mistakes"
                ]
        else:
            errors={}

        # build the form that gathers the expense info
        form = document.form(
            name='expense', legend="Enter expense information", action=context.cgihome)
        targetActor = form.hidden(name="actor", value=actor)
        targetRoutine = form.hidden(name="routine", value="submit")
        user = form.hidden(name="sentry.username", value=sentry.username)
        ticket = form.hidden(name="sentry.ticket", value=sentry.ticket)
        if defaults.id:
            eid = form.hidden(name="%s.id" % actor, value=defaults.id)

        # create the date picker
        dateAction="; ".join([
            'var cal = new CalendarPopup()',
            'cal.select(this, "date", "yyyy/MM/dd")',
            'return false'
            ])
        datePick = form.text(
            id='date', name='%s.date' % actor, label='Date:',
            size="10",
            value=defaults.date, title="yyyy/mm/dd",
            onClick=dateAction
            )
        datePick.help = "Click to bring up the calendar tool"

        # create the amount field
        if new:
            value = ''
        else:
            value = "%s" % defaults.amount
        amount = form.text(
            id='amount', name='%s.amount' % actor, label='Amount:',
            value=value
            )
        amount.help = " ".join([
            "Please enter the amount of the expense in USD.",
            "If the original amount is in a foreign currency, make sure that you",
            "follow company guidelines while performing the conversion."
            "Make sure you enter a number without the dollar sign."
            ])
        if "amount" in errors:
            amount.error = errors["amount"]

        # create the charge code selector widget
        codes = clerk.indexAllowedProjectCodes(sentry.username)
        if defaults.code:
            selection = defaults.code
        else:
            selection=None
        chargeCodeSelector = ent.content.chargeCodeSelector(
            id="chargeCode", name="%s.code" % actor,
            label="Charge code:", selected=selection,
            codes=codes
            )
        chargeCodeSelector.help = 'Please select a charge code from the list'
        form.field(control=chargeCodeSelector)
        if "code" in errors:
            chargeCodeSelector.error = errors["code"]

        # create the category selector widget
        codes = clerk.indexAllowedCategories(sentry.username)
        if defaults.category:
            selection = defaults.category
        else:
            selection=None
        categorySelector = ent.content.categorySelector(
            id="category", name="%s.category" % actor,
            label="Charge category:", selected=selection,
            codes=codes
            )
        categorySelector.help = 'Please select an expense category from the list'
        form.field(control=categorySelector)
        if "category" in errors:
            categorySelector.error = errors["category"]

        # create the description field
        if new:
            value = ''
        else:
            value = defaults.description
            
        description = form.text(
            id='description', name='%s.description' % actor, label='Description:',
            size="80",
            value=value
            )
        description.help = (
            "Please describe the reason for the expense. "
            "This field is required only for meals that involve third parties "
            "and as clarification when you have selected 'Other' as the charge "
            "category."
            )

        if "description" in errors:
            description.error = errors["description"]

        # the submit button
        submit = form.control(name="submit", type="submit", value="submit")

        return


    def timechargeForm(self, actor, context, document, defaults, errors):
        import ent.content
        
        # get access to the app context
        clerk = context.clerk
        sentry = context.sentry

        if errors:
            p = document.paragraph(cls="error")
            p.text = [
                "The form you filled out contained some errors.",
                "Please look through the data you have entered and correct any mistakes"
                ]

        # build the form that gathers the expense info
        form = document.form(
            name='timecharge', legend="Enter time charge information", action=context.cgihome)
        targetActor = form.hidden(name="actor", value=actor)
        targetRoutine = form.hidden(name="routine", value="submit")
        user = form.hidden(name="sentry.username", value=sentry.username)
        ticket = form.hidden(name="sentry.ticket", value=sentry.ticket)
        if defaults.id:
            eid = form.hidden(name="%s.id" % actor, value=defaults.id)

        # create the date picker
        dateAction=" ".join([
            'var cal = new CalendarPopup();',
            'cal.select(this, "date", "yyyy/MM/dd");',
            'return false;'
            ])
        datePick = form.text(
            id='date', name='%s.date' % actor, label='Date:',
            size="10",
            value=defaults.date, title="yyyy/mm/dd",
            onClick=dateAction
            )
        datePick.help = "Click to bring up the calendar tool"

        # create the amount field
        if defaults.duration:
            selection = "%.2f" % defaults.duration
        else:
            selection = None
        durationSelector = ent.content.durationSelector(
            id="duration", name="%s.duration" % actor,
            label="Duration:", selected=selection
            )
        durationSelector.help = 'Please select a duration from the list'
        form.field(control=durationSelector)
        
        # create the charge code selector widget
        codes = clerk.indexAllowedProjectCodes(sentry.username)
        if defaults.code:
            selection = defaults.code
        else:
            selection=None
        chargeCodeSelector = ent.content.chargeCodeSelector(
            id="chargeCode", name="%s.code" % actor,
            label="Charge code:", selected=selection,
            codes=codes
            )
        chargeCodeSelector.help = 'Please select a charge code from the list'
        form.field(control=chargeCodeSelector)

        # create the description field
        description = form.text(
            id='description', name='%s.description' % actor, label='Description:',
            size="80",
            value=defaults.description
            )
        description.help = "Please enter a short descriptin of the task"
        if "description" in errors:
            description.error = errors["description"]

        # the submit button
        submit = form.control(name="submit", type="submit", value="submit")

        return


    def projectForm(self, actor, context, document, defaults, errors, new=True):
        import ent.content

        # get access to the app content
        sentry = context.sentry
        clerk = context.clerk

        locations = clerk.indexLocations()

        # warn about any errors:
        if errors:
            p = document.paragraph(cls="error")
            p.text = [
                "The information you provided contained some errors.",
                "Please look through the fields you entered and corerct any mistakes"
                ]

        # build the form that gathers the project info
        form = document.form(
            name='project', legend='Enter project code imformation', action=context.cgihome)

        # first, the hidden fields
        targetActor = form.hidden(name="actor", value=actor)
        targetRoutine = form.hidden(name="routine", value="saveProject")
        new = form.hidden(name="%s.new" % actor, value=new)
        user = form.hidden(name="sentry.username", value=sentry.username)
        ticket = form.hidden(name="sentry.ticket", value=sentry.ticket)

        # project code
        code = form.text(
            id='id', name='%s.id' % actor, label="Project code:",
            value="%s" % defaults.id,
            required=True
            )
        code.help = "Enter the project code, e.g. OCC 001"
        if "id" in errors:
            code.error = errors["id"]
        
        # project location
        if defaults.location:
            selection = defaults.location
        else:
            selection = None
        location = ent.content.locationSelector(
            id="location", name="%s.location" % actor,
            label="Project location:", selected=selection,
            locations=locations
            )
        location.help = "Choose the OCC office that will run this project:"
        form.field(control=location, required=True)
        if "location" in errors:
            location.error = errors["location"]
        
        # project description
        description = form.text(
            id='description', name='%s.description' % actor, label="Project description:",
            value="%s" % defaults.description,
            required=True
            )
        description.help = "Enter the project description that will show up when entering expenses"
        if "description" in errors:
            description.error = errors["description"]
        
        # project client
        client = form.text(
            id='client', name='%s.client' % actor, label="Client:",
            value="%s" % defaults.client,
            required=True
            )
        client.help = "Enter the client name, e.g. OCC"
        if "client" in errors:
            client.error = errors["client"]
        
        contact = form.textarea(
            required=True,
            id='contact', name='%s.contact' % actor, label='Billing information:',
            cols='50', rows='5', wrap='soft',
            default=defaults.contact
            )
        contact.help = " ".join([
            "Please enter the name and address of the POC for invoice purposes.",
            "Use as many lines as necessary."
            ])
        if "contact" in errors:
            contact.error = errors["contact"]
        
        value = defaults.po
        if not value:
            value = ""
        po = form.text(
            id='po', name='%s.po' % actor, label="Purchase order number:",
            value="%s" % value,
            )
        po.help = "Please enter the PO number, if available"
        if "po" in errors:
            po.error = errors["po"]
        
        # the submit button
        submit = form.control(name="submit", type="submit", value="submit")

        return


    def renderProjects(self, director, document, projects, editable=False):
        #
        sentry = director.sentry
        
        # if none, say so and return
        if not projects:
            p = document.paragraph()
            p.text = [
                "There are no projects to list"
                ]
            return

        p = document.paragraph()
        p.text = [
            "The following tables show details for all relevant projects."
            ]
        if editable:
            p.text += [
                "You can edit the project information by following the links",
                "in the columns with project codes."
                ]

        section = document.document(title="Client billable projects")

        # first client billable projects
        table = section.literal()
        text = [
            '<p>',
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th>&nbsp;</th>',
            '      <th>Code</th>',
            '      <th>Client</th>',
            '      <th>Location</th>',
            '      <th>Description</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        index = 0
        for t in projects:
            if not t.billable:
                continue
            
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            if editable:
                actions = [
                    "actor=projectManager",
                    "routine=editProject",
                    "projectManager.id=%s" % t.id,
                    "sentry.username=%s" % sentry.username,
                    "sentry.ticket=%s" % sentry.ticket,
                    ]
                link = '<a href="%s?%s">%s</a>' % (director.cgihome, "&".join(actions), t.id)
            else:
                #link = '%s' % (index+1)
                link = '%s' % t.id

            text += [
                '    <tr class="%s">' % marker,
                '      <td class="index">%s</td>' % (index+1),
                '      <td class="text">%s</td>' % link,
                '      <td class="text">%s</td>' % t.client,
                '      <td class="text">%s</td>' % t.location,
                '      <td class="text">%s</td>' % t.description,
                '    </tr>',
                ]

            index += 1

        text += [
            '  </tbody>',
            '</table>',
            '</p>',
            ]

        table.text = text

        # now, OC&C internal projects
        section = document.document(title="OC&amp;C internal project codes")

        table = section.literal()
        text = [
            '<p>',
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th>&nbsp;</th>',
            '      <th>Code</th>',
            '      <th>Client</th>',
            '      <th>Location</th>',
            '      <th>Description</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        index = 0
        for t in projects:
            if t.billable:
                continue
            
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            text += [
                '    <tr class="%s">' % marker,
                '      <td class="index">%s</td>' % (index + 1),
                '      <td class="text">%s</td>' % t.id,
                '      <td class="text">%s</td>' % t.client,
                '      <td class="text">%s</td>' % t.location,
                '      <td class="text">%s</td>' % t.description,
                '    </tr>',
                ]
            index += 1

        text += [
            '  </tbody>',
            '</table>',
            '</p>',
            ]

        table.text = text

        return


    def renderReimbursementsReport(self, director, document, reports):
        clerk = director.clerk
        sentry = director.sentry
        
        # index employees
        employees = clerk.indexEmployees()

        # start building the table
        p = document.paragraph()
        p.text = [
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th>&nbsp;</th>',
            '      <th>Employee</th>',
            '      <th>Submitted</th>',
            '      <th>Total</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        total = 0.0
        for index, report in enumerate(reports):
            userTotal = 0.0
            expenses = clerk.retrieveReportedExpenses(report.id)
            fullname = employees[report.employee].fullname
            for expense in expenses:
                userTotal += expense.amount

            # compute the row marker
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            # create the link to the expense report detail
            actions = [
                "actor=reporter",
                "routine=viewExpenseReportDetails",
                "reporter.tag=%s" % report.id,
                "sentry.username=%s" % sentry.username,
                "sentry.ticket=%s" % sentry.ticket,
                ]
            link = '<a href="%s?%s">%s</a>' % (director.cgihome, "&".join(actions), report.id)

            # render the row
            p.text += [
                '    <tr class="%s">' % marker,
                '      <td class="text">%s</td>' % link,
                '      <td class="text">%s</td>' % fullname,
                '      <td class="date">%s</td>' % report.submitted,
                '      <td class="number">$%.2f</td>' % userTotal,
                '    </tr>',
                ]

            total += userTotal

        p.text += [
            '    <tr class="footer">',
            '      <td>&nbsp;</td>',
            '      <td class="total" colspan=2>',
            '        Total:',
            '      </td>',
            '      <td class="number">$%.2f</td>' % total,
            '    </tr>',
            '  </tbody>',
            '</table>',
            ]

        return


    def renderExpensesByDate(self, director, content, expenses):
        # gain access to the application contex
        clerk = director.clerk

        # index charge categories
        categories = {}

        # prepare our table
        index = {}

        # sum up the expenses in a given project and given category by date
        for expense in expenses:
            projectIndex = index.setdefault(expense.code, {})
            
            dateIndex = projectIndex.setdefault(expense.date, {})
            categoryTotal = dateIndex.setdefault(expense.category, 0.0)
            categoryTotal += expense.amount
            dateIndex[expense.category] = categoryTotal

            categoryIndex = categories.setdefault(expense.code, {})
            categoryIndex[expense.category] = None

        # loop over charged projects
        projects = index.keys()
        projects.sort()

        for projectId in projects:
            categoryTotals = {}
            
            p = content.paragraph()
            p.text = [
                'Project <strong>%s</strong>:' % projectId
                ]

            # figure out the row headers
            dates = index[projectId].keys()
            dates.sort()

            # create the category names header entries
            chargeCategories = categories[projectId].keys()
            chargeCategories.sort()
            categoryNames = "".join(
                [ "<th>%s</th>" % category for category in chargeCategories ])

            p = content.paragraph()
            p.text = [
                '<table cellspacing="0" class="table">',
                '  <thead>',
                '    <tr class="header">',
                '      <th>Date</th>',
                categoryNames,
                '      <th>Total</th>',
                '    </tr>',
                '  </thead>',
                '  <tbody>',
                ]

            for counter, date in enumerate(dates):
                # compute the row marker
                if counter % 2:
                    marker = "odd"
                else:
                    marker = "even"
                    
                data = []
                dateTotal = 0.0
                for category in chargeCategories:
                    try:
                        amount = index[projectId][date][category]

                        dateTotal += amount
                        categoryTotal = categoryTotals.setdefault(category, 0.0)
                        categoryTotal += amount
                        categoryTotals[category] = categoryTotal
                        
                        data.append('<td class="number">$%.2f</td>' % amount)
                    except KeyError:
                        data.append('<td>&nbsp;</td>')

                t = '<td class="total">$%.2f</td>' % dateTotal
                p.text += [
                    '<tr class="%s"><td>%s</td>%s</td>%s' % (marker, date, "".join(data), t)
                    ]

            reportTotal = 0.0
            totals = []
            for category in chargeCategories:
                try:
                    amount = categoryTotals[category]
                    reportTotal += amount
                    totals.append('<td class="total">$%.2f</td>' % amount)
                except KeyError:
                    totals.append('<td>&nbsp;</td>')

            p.text += [
                '    <tr class="footer">',
                '      <td>&nbsp;</td>',
                "".join(totals),
                '      <td class="total">$%.2f</td>' % reportTotal,
                '    </tr>',
                '  </tbody>',
                '</table>',
                ]

        return


    def renderExpensesByProject(self, director, content, project, bins, employees, table):

        # prepare the table columns
        employeeNames = "".join(
            ['<th class="verticalText">%s</th>' % name for name in employees])
        
        # prepare the table rows
        dates = table.keys()
        dates.sort()

        # totals for each employee
        totals = {}
        for employee in employees:
            totals[employee] = 0.0

        # start building the content
        p = content.paragraph()
        p.text = [
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th>%s</th>' % project,
            employeeNames,
            '      <th>Total</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        for index, bin in enumerate(bins):

            # bin label
            label = bin[0]
            
            # compute the row marker
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            total = 0.0
            record = []
            for employee in employees:
                duration = table[label][employee]
                total += duration
                totals[employee] += duration
                if duration:
                    field = "$%.2f" % duration
                else:
                    field = "&nbsp;"
                record.append('<td class="number">%s</td>' % field)
            record.append('<td class="total">$%.2f</td>' % total)
            entry = "".join(record)
                
            p.text += [
                '    <tr class="%s">' % marker,
                '      <td class="text">%s</td>' % label,
                entry,
                '    </tr>',
                ]

        # add the bottom of the table
        grandTotal = 0
        record = []
        for employee in employees:
            total = totals[employee]
            grandTotal += total
            record.append('<td class="total">$%.2f</td>' % total)
        record.append('<td class="total">$%.2f</td>' % grandTotal)
        entry = "".join(record)

        p.text += [
            '    <tr class="footer">',
            '      <td class="total">Totals:</td>',
            entry,
            '    </tr>',
            '  </tbody>',
            '</table>',
            ]

        return
    

    def renderTimeReports(self, director, document, reports):
        # gain access to the application context
        clerk = director.clerk
        sentry = director.sentry

        # prepare the indices
        employees = clerk.indexEmployees()

        # start building the table
        p = document.paragraph()
        p.text = [
            '<p>',
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th>&nbsp;</th>',
            '      <th>Employee</th>',
            '      <th>Submitted</th>',
            '      <th>Total</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        for index, report in enumerate(reports):
            userTotal = 0.0
            charges = clerk.retrieveReportedTimeCharges(report.id)
            fullname = employees[report.employee].fullname
            for charge in charges:
                userTotal += charge.duration

            # compute the row marker
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            # create the link to the time report detail
            actions = [
                "actor=reporter",
                "routine=viewTimeChargeReportDetails",
                "reporter.tag=%s" % report.id,
                "sentry.username=%s" % sentry.username,
                "sentry.ticket=%s" % sentry.ticket,
                ]
            link = '<a href="%s?%s">%s</a>' % (director.cgihome, "&".join(actions), report.id)

            # render the row
            p.text += [
                '    <tr class="%s">' % marker,
                '      <td class="text">%s</td>' % link,
                '      <td class="text">%s</td>' % fullname,
                '      <td class="date">%s</td>' % report.submitted,
                '      <td class="number">%.2f</td>' % userTotal,
                '    </tr>',
                ]

        p.text += [
            '  </tbody>',
            '</table>',
            ]

        return


    def renderTimeChargesByProject(self, director, content, project, bins, employees, table):

        # gain access to the application contex
        clerk = director.clerk

        # prepare the indices
        projectIndex = clerk.indexProjects()
        employeeIndex = clerk.indexEmployees()

        # prepare the table columns
        employeeNames = "".join(
            ['<th class="verticalText">%s</th>' % name for name in employees])
        
        # prepare the table rows
        dates = table.keys()
        dates.sort()

        # totals for each employee
        totals = {}
        for employee in employees:
            totals[employee] = 0.0

        # start building the content
        p = content.paragraph()
        p.text = [
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th>%s</th>' % project,
            employeeNames,
            '      <th>Total</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        for index, bin in enumerate(bins):

            # bin label
            label = bin[0]
            
            # compute the row marker
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            total = 0.0
            record = []
            for employee in employees:
                duration = table[label][employee]
                total += duration
                totals[employee] += duration
                if duration:
                    field = "%.2f" % duration
                else:
                    field = "&nbsp;"
                record.append('<td class="number">%s</td>' % field)
            record.append('<td class="total">%.2f</td>' % total)
            entry = "".join(record)
                
            p.text += [
                '    <tr class="%s">' % marker,
                '      <td class="text">%s</td>' % label,
                entry,
                '    </tr>',
                ]

        # add the bottom of the table
        grandTotal = 0
        record = []
        for employee in employees:
            total = totals[employee]
            grandTotal += total
            record.append('<td class="total">%.2f</td>' % total)
        record.append('<td class="total">%.2f</td>' % grandTotal)
        entry = "".join(record)

        p.text += [
            '    <tr class="footer">',
            '      <td class="total">Totals:</td>',
            entry,
            '    </tr>',
            '  </tbody>',
            '</table>',
            ]

        return
    

    def renderTimeChargesByEmployee(self, director, content, employee, bins, projects, table):
        # prepare the table columns
        projectNames = "".join(
            ['<th class="verticalText">%s</th>' %
             "&nbsp;".join(name.split()) for name in projects])
        
        # prepare the table rows
        dates = table.keys()
        dates.sort()

        # totals for each project
        totals = {}
        for project in projects:
            totals[project] = 0.0

        # start building the content
        p = content.paragraph()
        p.text = [
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th>%s</th>' % employee,
            projectNames,
            '      <th>Total</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        for index, bin in enumerate(bins):

            # bin label
            label = bin[0]
            
            # compute the row marker
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            total = 0.0
            record = []
            for project in projects:
                duration = table[label][project]
                total += duration
                totals[project] += duration
                if duration:
                    field = "%.2f" % duration
                else:
                    field = "&nbsp;"
                record.append('<td class="number">%s</td>' % field)
            record.append('<td class="total">%.2f</td>' % total)
            entry = "".join(record)
                
            p.text += [
                '    <tr class="%s">' % marker,
                '      <td class="text">%s</td>' % label,
                entry,
                '    </tr>',
                ]

        # add the bottom of the table
        grandTotal = 0
        record = []
        for project in projects:
            total = totals[project]
            grandTotal += total
            record.append('<td class="total">%.2f</td>' % total)
        record.append('<td class="total">%.2f</td>' % grandTotal)
        entry = "".join(record)

        p.text += [
            '    <tr class="footer">',
            '      <td class="total">Totals:</td>',
            entry,
            '    </tr>',
            '  </tbody>',
            '</table>',
            ]

        return
    

    def selectExpenseReports(self, actor, director, document, reports, checked=False):
        clerk = director.clerk
        sentry = director.sentry
        
        # index employees
        employees = clerk.indexEmployees()

        # build the form that gathers the expense info
        form = document.form(
            name='expense', legend="Select expense reports to pay", action=director.cgihome,
            onSubmit= (
                'return gatherCheckboxes('
                'this.elements["expenseReports"], this.elements["%s.reports"]);' % actor
                )
            )
        targetActor = form.hidden(name="actor", value=actor)
        targetRoutine = form.hidden(name="routine", value="reimburseExpenseReports")
        targetReports = form.hidden(name="%s.reports" % actor, value="")
        user = form.hidden(name="sentry.username", value=sentry.username)
        ticket = form.hidden(name="sentry.ticket", value=sentry.ticket)

        # create the description field
        description = form.text(
            id='description', name='%s.description' % actor, label='Description:',
            size="80", value=""
            )
        description.help = (
            "Please enter an optional comment about this reimbursement."
            )

        # start building the table
        p = form.paragraph()
        p.text = [
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th><img src="images/linkOpaque.gif"'
            '          onClick="flipCheckboxes('
            '              document.forms[\'expense\'].elements[\'expenseReports\'])'
            '          ">'
            '      </th>',
            '      <th>&nbsp;</th>',
            '      <th>Employee</th>',
            '      <th>Submitted</th>',
            '      <th>Amount</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        total = 0.0
        for index, report in enumerate(reports):
            userTotal = 0.0
            expenses = clerk.retrieveReportedExpenses(report.id)
            fullname = employees[report.employee].fullname
            for expense in expenses:
                userTotal += expense.amount

            # compute the row marker
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            # create the link to the expense report detail
            actions = [
                "actor=reporter",
                "routine=viewExpenseReportDetails",
                "reporter.tag=%s" % report.id,
                "sentry.username=%s" % sentry.username,
                "sentry.ticket=%s" % sentry.ticket,
                ]
            link = '<a href="%s?%s">%s</a>' % (director.cgihome, "&".join(actions), report.id)

            if checked:
                status = " checked"
            else:
                status = ""
            selector = '<input %s type="checkbox" name="expenseReports" id="%s">' % (
                status, report.id)

            # render the row
            p.text += [
                '    <tr class="%s">' % marker,
                '      <td>%s</td>' % selector,
                '      <td class="text">%s</td>' % link,
                '      <td class="text">%s</td>' % fullname,
                '      <td class="date">%s</td>' % report.submitted,
                '      <td class="number">$%.2f</td>' % userTotal,
                '    </tr>',
                ]

            total += userTotal

        p.text += [
            '    <tr class="footer">',
            '      <td>&nbsp;</td>',
            '      <td>&nbsp;</td>',
            '      <td class="total" colspan=2>',
            '        Total:',
            '      </td>',
            '      <td class="number">$%.2f</td>' % total,
            '    </tr>',
            '  </tbody>',
            '</table>',
            ]

        # the submit button
        submit = form.control(name="submit", type="submit", value="submit")

        return


    def renderReimbursements(self, director, section, reimbursements):
        sentry = director.sentry

        # start building the table
        p = section.paragraph()
        p.text = [
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th>&nbsp;</th>',
            '      <th>Submitted</th>',
            '      <th>Approved</th>',
            '      <th>Description</th>',
            '      <th>Status</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        for index, report in enumerate(reimbursements):
            # compute the row marker
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            # create the link to the expense report detail
            actions = [
                "actor=accountant",
                "routine=prepareReimbursementCollateral",
                "accountant.reimbursement=%s" % report.id,
                "sentry.username=%s" % sentry.username,
                "sentry.ticket=%s" % sentry.ticket,
                ]
            link = '<a href="%s?%s">%s</a>' % (
                director.cgihome, "&".join(actions), report.id)

            description = report.description
            if not description:
                description = "&nbsp;"

            # render the row
            p.text += [
                '    <tr class="%s">' % marker,
                '      <td class="text">%s</td>' % link,
                '      <td class="date">%s</td>' % report.submitted,
                '      <td class="text">%s</td>' % report.approved,
                '      <td class="text">%s</td>' % description,
                '      <td class="status">%s</td>' % report.status,
                '    </tr>',
                ]

        p.text += [
            '    <tr class="footer">',
            '      <td>&nbsp;</td>',
            '      <td>&nbsp;</td>',
            '      <td>&nbsp;</td>',
            '      <td>&nbsp;</td>',
            '      <td>&nbsp;</td>',
            '    </tr>',
            '  </tbody>',
            '</table>',
            ]

        return


    def renderInvoice(self, actor, director, document, invoice, editable=True):
        clerk = director.clerk
        sentry = director.sentry
        project = clerk.retrieveProject(invoice.project)

        items = clerk.retrieveInvoicedItems(invoice.id)

        contact = "<br>".join(project.contact.splitlines())
        po = project.po

        p = document.literal()
        p.text = [
            '<p>',
            '<table width="100%" cellspacing="0">',
            '  <tbody>',
            '    <tr>',
            '      <td colspan="2">',
            '      <div><b>To:</b></div>',
            '      </td>',
            '      <td rowspan="2">',
            '      <div><b>Invoice:</b> %s</div>' % invoice.code,
            '      <div><b>Date:</b> %s</div>' % invoice.date,
            '      <div><b>RE: %s</b></div>' % po,
            '      <div><br>%s</div>' % invoice.ref,
            '      </td>',
            '    </tr>',
            '    <tr>',
            '      <td width="1%">&nbsp;</td>',
            '      <td>',
            '      <div>%s</div>' % contact,
            '      </td>',
            '    </tr>',
            ]

        p.text += [
            '  </tbody>',
            '</table>',
            '</p>',
            ]
        
        if not items:
            p = document.paragraph(cls="error")
            p.text = [
                "Invoice <b>%s</b> has no associated line items!" % invoice.code
                ]

            if invoice.status == 'a':
                form = document.form(
                    name="invoiceDetails", action=director.cgihome,
                    )

                form.hidden(name="actor", value=actor)
                form.hidden(name="routine", value="collectLineItem")
                form.hidden(name="%s.invoice" % actor, value=invoice.id)
                form.hidden(name="sentry.username", value=sentry.username)
                form.hidden(name="sentry.ticket", value=sentry.ticket)

                # add the submit button
                submit = form.submitButton(value="add a line item")

            return
        
        p = document.literal()
        p.text = [
            '<p>',
            '<table width="100%" cellspacing="0" class="invoice">',
            '  <thead>',
            '    <tr class="header">',
            '      <th width="1%">&nbsp;</th>',
            '      <th width="98%">Description</th>',
            '      <th width="1%">Amount</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        total = 0.0
        for index, item in enumerate(items):
            amount = item.amount
            total += amount

            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            if editable:
                actions = [
                    "actor=invoiceMaker",
                    "routine=editLineItem",
                    "invoiceMaker.item=%s" % item.id,
                    "sentry.username=%s" % sentry.username,
                    "sentry.ticket=%s" % sentry.ticket,
                    ]
                link = '<a href="%s?%s">%s</a>' % (director.cgihome, "&".join(actions), index+1)
            else:
                link = '%s' % (index+1)

            p.text += [
                '    <tr class="%s">' % marker,
                '      <td class="index">%s</td>' % link,
                '      <td class="text">',
                '        <div class="description">',
                item.description,
                '        </div>',
                '        <div class="detail">',
                item.detail,
                '        </div>',
                '      </td>',
                '      <td class="number">%-.2f</td>' % amount,
                '    </tr>'
                ]

        p.text += [
            '    <tr class="footer">',
            '      <td>&nbsp;</td>',
            '      <td class="total">',
            '        Total:',
            '      </td>',
            '      <td class="number">%.2f</td>' % total,
            '  </tbody>',
            '</table>',
            '</p>',
            ]


        if invoice.status == 'a':
            form = document.form(
                name="invoiceDetails", action=director.cgihome,
                )

            form.hidden(name="actor", value=actor)
            form.hidden(name="routine", value="collectLineItem")
            form.hidden(name="%s.invoice" % actor, value=invoice.id)
            form.hidden(name="sentry.username", value=sentry.username)
            form.hidden(name="sentry.ticket", value=sentry.ticket)

            # add the submit button
            submit = form.submitButton(value="add a line item")

            form = document.form(
                name="invoiceSubmisson", action=director.cgihome,
                )

            form.hidden(name="actor", value=actor)
            form.hidden(name="routine", value="submitInvoice")
            form.hidden(name="%s.invoice" % actor, value=invoice.id)
            form.hidden(name="sentry.username", value=sentry.username)
            form.hidden(name="sentry.ticket", value=sentry.ticket)

            # add the submit button
            submit = form.submitButton(value="submit invoice")

        return


    def retrieveInvoices(self, actor, director, document, defaults, errors=None):
        # get access to the application context
        clerk = director.clerk
        sentry = director.sentry

        if errors:
            p = document.paragraph(cls="error")
            p.text = [
                "The form you filled out contained some errors.",
                "Please look through the data you have entered and correct any mistakes"
                ]
        else:
            errors={}

        # build the query form
        form = document.form(
            name='invoice_spec', legend="Search for invoices", action=director.cgihome)

        targetActor = form.hidden(name='actor', value=actor)
        targetRoutine = form.hidden(name='routine', value="retrieveInvoices")
        username = form.hidden(name='sentry.username', value=sentry.username)
        ticket = form.hidden(name='sentry.ticket', value=sentry.ticket)

        invoiceId = defaults.invoice
        enddate = defaults.enddate
        startdate = defaults.startdate

        invoiceSelector = form.text(
            id="invoice", name="%s.invoice" % actor, label="Invoice:",
            value=invoiceId
            )
        invoiceSelector.help = " ".join([
            "Please enter an invoice code. Partial entries will return",
            "all matching invoices"
            ])
          
        # create the date pickers
        dateAction=" ".join([
            'var cal = new CalendarPopup();',
            'cal.showYearNavigation();',
            'cal.select(this, "startdate", "yyyy/MM/dd");',
            'return false;'
            ])
        startdatePick = form.text(
            id='startdate', name='%s.startdate' % self.name, label='Submitted after:',
            size="10",
            value=startdate, title="yyyy/mm/dd",
            onClick=dateAction
            )
        startdatePick.help = "Click to bring up the calendar tool"

        dateAction=" ".join([
            'var cal = new CalendarPopup();',
            'cal.showYearNavigation();',
            'cal.select(this, "enddate", "yyyy/MM/dd");',
            'return false;'
            ])
        enddatePick = form.text(
            id='enddate', name='%s.enddate' % self.name, label='Submitted before:',
            size="10",
            value=enddate, title="yyyy/mm/dd",
            onClick=dateAction
            )
        enddatePick.help = "Click to bring up the calendar tool"

        submit = form.submitButton()

        criteria = []
        if invoiceId:
            criteria.append("code~'%s'" % invoiceId)
        if startdate:
            criteria.append("submitted>='%s'" % startdate)
        if enddate:
            criteria.append("submitted<='%s'" % enddate)
        if not criteria:
            return

        criteria += [
            "status!='a'"
            ]

        expr = " and ".join(criteria)
        invoices = clerk.retrieveInvoices(criteria=expr, sort="code,date")
        if not invoices:
            p = document.paragraph(cls="error")
            p.text = [
                "There are no invoices in the database that match your selection criteria."
                ]
            return

        if len(invoices) == 1:
            p = document.paragraph()
            p.text = [
                "Your search criteria matched invoice <b>%s</b>. Here are the associated details."
                ]
            invoice = invoices[0]
            self.renderInvoice(actor, director, document, invoice)
            return

        p = document.paragraph()
        p.text = [
            "The table below lists the invoices that matched your criteria.",
            "You can view the details of any of these invoices by cliking on the invoice number"
            ]

        self.renderInvoices(actor, director, document, invoices)

        return


    def renderInvoices(self, actor, director, document, invoices, editable=True):
        clerk = director.clerk
        sentry = director.sentry

        # start building the table
        p = document.paragraph()
        p.text = [
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th>&nbsp;</th>',
            '      <th>Invoice</th>',
            '      <th>Project</th>',
            '      <th>Submitted</th>',
            '      <th>Paid</th>',
            '      <th>Amount</th>',
            '      <th>Currency</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        total = {}
        for index, invoice in enumerate(invoices):
            invoiceTotal = 0.0

            items = clerk.retrieveInvoicedItems(invoice.id)
            for item in items:
                invoiceTotal += item.amount

            amount = total.setdefault(invoice.currency, 0.0)
            amount += invoiceTotal
            total[invoice.currency] = amount

            # compute the row marker
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            # create the link to the invoice detail
            if editable:
                actions = [
                    "actor=%s" % actor,
                    "routine=viewInvoice",
                    "%s.invoice=%s" % (actor, invoice.id),
                    "sentry.username=%s" % sentry.username,
                    "sentry.ticket=%s" % sentry.ticket,
                    ]
                link = '<a href="%s?%s">%s</a>' % (
                    director.cgihome, "&".join(actions), invoice.code)
            else:
                link = invoice.code

            paid = invoice.paid.strip()
            if not paid:
                paid = "&nbsp;"

            # render the row
            p.text += [
                '    <tr class="%s">' % marker,
                '      <td class="number">%s</td>' % (index+1),
                '      <td class="text">%s</td>' % link,
                '      <td class="text">%s</td>' % invoice.project,
                '      <td class="date">%s</td>' % invoice.date,
                '      <td class="date">%s</td>' % paid,
                '      <td class="number">%.2f</td>' % invoiceTotal ,
                '      <td class="text">%s</td>' % invoice.currency,
                '    </tr>',
                ]

        currencies = total.keys()
        currencies.sort()

        span = len(currencies)
        
        p.text += [
            '    <tr class="footer">',
            '      <td rowspan="%d">&nbsp;</td>' % span,
            '      <td class="total" rowspan="%d" colspan="4">Total:</td>' % span,
            ]

        lines = []
        for currency in currencies:
            lines.append("".join([
                '<td class="number">%.2f</td>' % total[currency],
                '<td class="text">%s</td>' % currency,
                '</tr>',
                ]))
        rows = '<tr class="footer">'.join(lines)
            
        p.text += [
            rows,
            '  </tbody>',
            '</table>',
            ]

        return


    def selectInvoices(self, actor, routine, action, director, document, invoices, checked=False):
        clerk = director.clerk
        sentry = director.sentry
        
        if checked:
            status = " checked"
        else:
            status = ""

        # build the form that gathers the invoice info
        form = document.form(
            name='invoices',
            legend="Select invoices to %s" % action,
            action=director.cgihome,
            onSubmit= (
                'return gatherCheckboxes('
                'this.elements["invoiceEntry"], this.elements["%s.invoices"]);' % actor
                )
            )
        targetActor = form.hidden(name="actor", value=actor)
        targetRoutine = form.hidden(name="routine", value=routine)
        targetReports = form.hidden(name="%s.invoices" % actor, value="")
        user = form.hidden(name="sentry.username", value=sentry.username)
        ticket = form.hidden(name="sentry.ticket", value=sentry.ticket)

        # start building the table
        p = form.paragraph()
        p.text = [
            '<table cellspacing="0" class="table">',
            '  <thead>',
            '    <tr class="header">',
            '      <th colspan="3">&nbsp;</th>',
            '      <th colspan="2">Submitted</th>',
            '      <th colspan="2">&nbsp;</th>',
            '    </tr>',
            '    <tr class="header">',
            '      <th><img src="images/linkOpaque.gif"'
            '          onClick="flipCheckboxes('
            '              document.forms[\'invoices\'].elements[\'invoiceEntry\'])'
            '          ">'
            '      </th>',
            '      <th>Invoice</th>',
            '      <th>Project</th>',
            '      <th>by</th>',
            '      <th>on</th>',
            '      <th colspan="2">Amount</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        total = {}
        for index, invoice in enumerate(invoices):
            invoiceTotal = 0.0

            items = clerk.retrieveInvoicedItems(invoice.id)
            for item in items:
                invoiceTotal += item.amount

            amount = total.setdefault(invoice.currency, 0.0)
            amount += invoiceTotal
            total[invoice.currency] = amount

            # compute the row marker
            if index % 2:
                marker = "odd"
            else:
                marker = "even"

            # create the link to the invoice detail
            actions = [
                "actor=%s" % actor,
                "routine=viewInvoice",
                "%s.invoice=%s" % (actor, invoice.id),
                "sentry.username=%s" % sentry.username,
                "sentry.ticket=%s" % sentry.ticket,
                ]
            link = '<a href="%s?%s">%s</a>' % (director.cgihome, "&".join(actions), invoice.code)

            if invoice.status != 'p':
                selector = '<input %s type="checkbox" name="invoiceEntry" id="%s">' % (
                    status, invoice.id)
            else:
                selector = '&nbsp;&#10003;'
                selector = '&nbsp;'

            #marker = self._currencyMarker(invoice.currency)
            marker = invoice.currency
            amountStr = invoiceTotal
            amountStr = self._renderers[invoice.currency](invoiceTotal)
                
            # render the row
            p.text += [
                '    <tr class="%s">' % marker,
                '      <td>%s</td>' % selector,
                '      <td class="text">%s</td>' % link,
                '      <td class="text">%s</td>' % invoice.project,
                '      <td class="date">%s</td>' % invoice.creator,
                '      <td class="date">%s</td>' % invoice.date,
                #'      <td class="number">%s&nbsp;%.2f</td>' % (marker, invoiceTotal),
                '      <td class="number">%s</td>' % amountStr,
                '      <td class="number">%s</td>' % marker,
                '    </tr>',
                ]

        currencies = total.keys()
        currencies.sort()

        span = len(currencies)
        
        p.text += [
            '    <tr class="footer">',
            '      <td rowspan="%d">&nbsp;</td>' % span,
            '      <td class="total" rowspan="%d" colspan="4">' % span,
            '        Total:',
            '      </td>',
            ]

        lines = []
        for currency in currencies:
            #marker = self._currencyMarker(currency)
            marker = currency
            amountStr = total[currency]
            amountStr = self._renderers[currency](total[currency])
            lines.append("".join([
                # '<td class="number">%s&nbsp;%.2f</td>' % (marker, amountStr),
                '<td class="number">%s</td>' % amountStr,
                '<td class="text">%s</td>' % marker,
                '</tr>',
                ]))
        rows = '<tr class="footer">'.join(lines)
            
        p.text += [
            rows,
            '  </tbody>',
            '</table>',
            ]

        # the submit button
        submit = form.control(name="submit", type="submit", value=action)

        return


    def collectInvoiceData(self, actor, director, document, defaults, errors=None):

        import ent.content
        sentry = director.sentry

        if errors:
            p = document.paragraph(cls="error")
            p.text = [
                "The form you filled out contained some errors.",
                "Please look through the data you have entered and correct any mistakes"
                ]
        else:
            errors={}

        p = document.paragraph()
        p.text = [
            "Please select a project code from the drop down list and provide a short",
            "description of the contents of this invoice"
            ]

        # build the form that requests the project code
        form = document.form(
            name="projectCode", legend="Select a project code", action=director.cgihome)

        # first the hidden fields
        targetActor = form.hidden(name="actor", value=actor)
        targetRoutine = form.hidden(name="routine", value="getInvoiceContents")
        user = form.hidden(name="sentry.username", value=sentry.username)
        ticket = form.hidden(name="sentry.ticket", value=sentry.ticket)

        # create the charge code selector widget
        codes = director.clerk.indexActiveBillableProjects()
        if defaults.project:
            selection = defaults.project
        else:
            selection = None
        projectSelector = ent.content.chargeCodeSelector(
            id="project", name="%s.project" % actor,
            label="Project:", selected=selection,
            codes=codes
            )
        projectSelector.help = 'Please select a charge code from the list'
        if "project" in errors:
            projectSelector.error = errors["project"]
        form.field(control=projectSelector, required=True)

        # create the date picker
        datevalue = defaults.date
        if not datevalue:
            import time
            datevalue = time.strftime("%Y/%m/%d")
        dateAction="; ".join([
            'var cal = new CalendarPopup()',
            'cal.select(this, "date", "yyyy/MM/dd")',
            'return false'
            ])
        datePick = form.text(
            required=True,
            id='date', name='%s.date' % actor, label='Invoice date:',
            size="10",
            value=datevalue, title="yyyy/mm/dd",
            onClick=dateAction
            )
        datePick.help = "Click to bring up the calendar tool"

        ref = form.textarea(
            required=True,
            id='ref', name='%s.ref' % actor, label='RE:',
            cols='50', rows='5', wrap='soft',
            default=defaults.ref
            )
        ref.help = " ".join([
            "Please enter a short description of the contents of this invoice",
            "Use as many lines as necessary."
            ])
        if "ref" in errors:
            ref.error = errors["ref"]

        p = form.paragraph(cls="success")
        p.text = [
            "Please specify the payment details for this invoice"
            ]

        if defaults.office:
            selection = defaults.office
        else:
            selection = None
        locations = director.clerk.indexLocations()
        locationSelector = ent.content.locationSelector(
            id="office", name="%s.office" % actor,
            label="Office:", selected=selection,
            locations=locations
            )
        locationSelector.help = " ".join([
            "Please specify where payments should be mailed to",
            "in case the client pays by check."
            ])
        if "location" in errors:
            locationSelector.error = errors["location"]
        form.field(control=locationSelector, required=True)
            
        if defaults.currency:
            selection = defaults.currency
        else:
            selection=None
        currencySelector = ent.content.currencySelector(
            id="currency", name="%s.currency" % actor,
            label="Currency:", selected=selection
            )
        currencySelector.help = 'Please select the invoice currency from the list'
        if "currency" in errors:
            currencySelector.error = errors["currency"]
        form.field(control=currencySelector, required=True)

        submit = form.submitButton()

        return


    def collectInvoiceLineItem(self, actor, director, document, item, action="add", errors=None):

        import ent.content

        # get access to the app context
        clerk = director.clerk
        sentry = director.sentry

        if not errors:
            errors={}

        # get the invoice record
        invoice = clerk.retrieveInvoice(item.invoice)

        form = document.form(
            name="collectLineItem", action=director.cgihome,
            )

        form.hidden(name="actor", value=actor)
        form.hidden(name="routine", value="validateLineItem")
        form.hidden(name="%s.item" % actor, value=item.id)
        form.hidden(name="%s.invoice" % actor, value=item.invoice)
        form.hidden(name="sentry.username", value=sentry.username)
        form.hidden(name="sentry.ticket", value=sentry.ticket)

        description = form.textarea(
            required=True,
            id='description', name='%s.description' % actor, label='Line item description:',
            cols='80', rows='2', wrap='soft',
            default=item.description
            )
        description.help = " ".join([
            "Please enter a short description of this line item.",
            "Use as many lines as necessary."
            ])
        if "description" in errors:
            description.error = errors["description"]
            
        if item.amount:
            amount = "%.2f" % item.amount
        else:
            amount = ""
        amount = form.text(
            required=True,
            id='amount', name='%s.amount' % actor, label='Amount:',
            value=amount
            )
        amount.help = " ".join([
            "Please enter the line item amount in %s." % invoice.currency,
            "Make sure you enter just a number without any currency signs."
            ])
        if "amount" in errors:
            amount.error = errors["amount"]

        if item.category:
            selection = item.category
        else:
            selection=None
        categorySelector = ent.content.incomeSelector(
            id="category", name="%s.category" % actor,
            label="Income category:", selected=selection
            )
        categorySelector.help = 'Please select the income category from the list'
        form.field(control=categorySelector, required=True)

        detail = form.textarea(
            required=False,
            id='detail', name='%s.detail' % actor, label='Line item details:',
            cols='80', rows='2', wrap='soft',
            default=item.detail
            )
        detail.help = " ".join([
            "Please enter a detailed explanation for this line item.",
            "Use as many lines as necessary."
            ])
            
        # add the submit button
        submit = form.submitButton(value=action)

        return


    def __init__(self, name=None):
        if name is None:
            name = "scribe"
        super(Scribe, self).__init__(name, "scribe")

        self._renderers = {
            'EUR': self._eur,
            'USD': self._usd
            }

        return


    def _currencyMarker(self, currency):
        if currency == "EUR":
            marker = '&euro;'
        elif currency == "USD":
            marker = '$'
        else:
            marker = ''
                
        return marker


    def _usd(self, value):
        grps = []

        if value == 0.0:
            return "0.00"

        ip = int(value)
        fp =  round(100*(value - ip))
        while ip:
            ip, remainder = divmod(ip, 1000)
            grps.append(remainder)

        txt = ["%d" % grps[-1]] + [ "%03d" % grp for grp in reversed(grps[:-1]) ]
        return ",".join(txt) + '.' + "%02d"%fp 


    def _eur(self, value):
        grps = []

        if value == 0.0:
            return "0,00"

        ip = int(value)
        fp =  round(100*(value - ip))
        while ip:
            ip, remainder = divmod(ip, 1000)
            grps.append(remainder)

        txt = ["%d" % grps[-1]] + [ "%03d" % grp for grp in reversed(grps[:-1]) ]
        return ".".join(txt) + ',' + "%02d"%fp 


# version
__id__ = "$Id: Scribe.py,v 1.27 2008-02-21 10:02:22 aivazis Exp $"

# End of file 
