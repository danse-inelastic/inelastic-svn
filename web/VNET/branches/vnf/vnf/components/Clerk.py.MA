#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                               Orthologue, Ltd.
#                      (C) 2004-2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from DBAccessor import DBAccessor


class Clerk(DBAccessor):


    def indexProjects(self):
        """create an index of all project codes"""

        from ent.dom.Project import Project
        index = {}
        codes = self.db.fetchall(Project)
        for code in codes:
            index[code.id] = code

        return index


    def indexCategories(self):
        """create an index of all allowed charge categories for <username>"""

        from ent.dom.Category import Category
        index = {}
        codes = self.db.fetchall(Category)
        for code in codes:
            index[code.id] = code

        return index


    def indexActiveProjects(self):
        """create an index of all active project codes"""

        from ent.dom.Project import Project
        index = {}
        codes = self.db.fetchall(Project, where="status='a'")
        for code in codes:
            index[code.id] = code

        return index


    def indexActiveBillableProjects(self):
        """create an index of all active project codes"""

        from ent.dom.Project import Project
        index = {}
        criteria = [
            "status='a'",
            "billable=true",
            ]
        expr = " and ".join(criteria)
        codes = self.db.fetchall(Project, where=expr)
        for code in codes:
            index[code.id] = code

        return index


    def indexAllowedProjectCodes(self, username):
        """create an index of all allowed charge codes for <username>"""

        from ent.dom.Project import Project
        index = {}
        codes = self.db.fetchall(Project, where="status='a'")
        for code in codes:
            index[code.id] = code

        return index


    def indexAllowedCategories(self, username):
        """create an index of all allowed charge categories for <username>"""

        from ent.dom.Category import Category
        index = {}
        codes = self.db.fetchall(Category)
        for code in codes:
            index[code.id] = code

        return index


    def indexUsers(self, where=None):
        """create an index of all users that meet the specified criteria"""
    
        from ent.dom.User import User
        index = {}
        users = self.db.fetchall(User, where=where)
        for user in users:
            index[user.username] = user

        return index


    def indexActiveUsers(self):
        """create an index of all active users"""
        return self.indexUsers(where="status='a'")


    def indexEmployees(self):
        """create an index of all employees"""

        from ent.dom.Employee import Employee
        index = {}
        employees = self.db.fetchall(Employee)
        for employee in employees:
            index[employee.id] = employee

        return index


    def indexLocations(self):
        """create an index of all OC&C locations"""

        from ent.dom.Location import Location
        index = {}
        locations = self.db.fetchall(Location)
        for location in locations:
            index[location.id] = location

        return index


    def newExpense(self, expense):
        self.db.insertRow(expense)
        return


    def newTimeCharge(self, charge):
        self.db.insertRow(charge)
        return


    def newProject(self, project):
        self.db.insertRow(project)
        return


    def newReimbursement(self, reimbursement):
        self.db.insertRow(reimbursement)
        return


    def newInvoice(self, invoice):
        self.db.insertRow(invoice)
        return


    def newInvoicedItem(self, item):
        self.db.insertRow(item)
        return


    def newReimbursedReport(self, record):
        self.db.insertRow(record)
        return


    def updateExpense(self, expense):
        where = "id='%s'" % expense.id
        assignments = [
            ("date", expense.date),
            ("code", expense.code),
            ("amount", expense.amount),
            ("category", expense.category),
            ("description", expense.description),
            ]
        self.db.updateRow(expense, assignments, where)
        return


    def updateTimeCharge(self, charge):
        where = "id='%s'" % charge.id
        assignments = [
            ("date", charge.date),
            ("code", charge.code),
            ("duration", charge.duration),
            ("description", charge.description),
            ]
        self.db.updateRow(charge, assignments, where)
        return


    def updateProject(self, project):
        where = "id='%s'" % project.id
        assignments = [
            ("client", project.client),
            ("location", project.location),
            ("description", project.description),
            ("billable", project.billable),
            ("status", project.status),
            ("contact", project.contact),
            ("po", project.po),
            ]
        self.db.updateRow(project, assignments, where)
        return


    def updateInvoice(self, invoice):
        where = "id='%s'" % invoice.id
        assignments = [
            ("code", invoice.code),
            ("creator", invoice.creator),
            ("project", invoice.project),
            ("date", invoice.date),
            ("paid", invoice.paid),
            ("ref", invoice.ref),
            ("account", invoice.account),
            ("currency", invoice.currency),
            ("status", invoice.status),
            ]
        self.db.updateRow(invoice, assignments, where)
        return


    def updateInvoicedItem(self, item):
        where = "id='%s'" % item.id
        assignments = [
            ("id", item.id),
            ("invoice", item.invoice),
            ("amount", item.amount),
            ("category", item.category),
            ("description", item.description),
            ("detail", item.detail),
            ]
        self.db.updateRow(item, assignments, where)
        return


    def payExpenseReport(self, report):
        from ent.dom.ExpenseReport import ExpenseReport
        where = "id='%s'" % report
        assignments = [
            ("status", "p")
            ]

        self.db.updateRow(ExpenseReport, assignments, where)
        return


    def deleteExpense(self, tag):
        from ent.dom.Expense import Expense
        where = "id='%s'" % tag
        assignments = [
            ("status", "d"),
            ]
        self.db.updateRow(Expense, assignments, where)
        return


    def deleteTimeCharge(self, tag):
        from ent.dom.Time import Time
        where = "id='%s'" % tag
        assignments = [
            ("status", "d"),
            ]
        self.db.updateRow(Time, assignments, where)
        return


    def deleteInvoice(self, tag):
        from ent.dom.Invoice import Invoice
        from ent.dom.InvoicedItem import InvoicedItem

        self.db.deleteRow(InvoicedItem, where="invoice='%s'" % tag)
        self.db.deleteRow(Invoice, where="id='%s'" % tag)

        return


    def deleteInvoiceItem(self, tag):
        from ent.dom.InvoicedItem import InvoicedItem
        self.db.deleteRow(InvoicedItem, where="id='%s'" % tag)
        return


    def retrieveExpense(self, tag):
        """locate a particular expense given its id"""

        from ent.dom.Expense import Expense
        records = self.db.fetchall(Expense, where="id='%s'" % tag)

        # there had better only be one of these
        return records[0]


    def retrieveTimeCharge(self, tag):
        """locate a particular time charge given its id"""

        from ent.dom.Time import Time
        records = self.db.fetchall(Time, where="id='%s'" % tag)

        # there had better only be one of these
        return records[0]


    def retrieveProject(self, tag):
        """locate a particular project given its id"""

        from ent.dom.Project import Project
        records = self.db.fetchall(Project, where="id='%s'" % tag)

        # there had better only be one of these
        return records[0]


    def retrieveOutstandingExpenses(self, username, order="date"):
        """locate all expenses marked 'n' by this user"""

        from ent.dom.Expense import Expense
        records = self.db.fetchall(
            Expense,
            where="employee='%s' and status='n'" % username,
            sort=order)

        return records


    def retrieveExpenses(self, criteria, order):
        from ent.dom.Expense import Expense
        return self.db.fetchall(Expense, where=criteria, sort=order)


    def retrieveSubmittedExpenses(self, code=None, order="date"):
        """locate all submitted expenses"""

        if code is None:
            criterion = "status='s'"
        else:
            criterion = "code='%s' and status='s'" % code

        from ent.dom.Expense import Expense
        records = self.db.fetchall(Expense, where=criterion, sort=order)

        return records


    def retrieveReportedExpenses(self, report, order="date"):
        """locate all expenses associated with a given report confirmation code"""
        from ent.dom.Expense import Expense
        expenses = self.db.fetchall(
            Expense,
            where="id=ANY(SELECT expense from reported_expenses where report='%s')" % report,
            sort=order)
        
        return expenses


    def retrieveReportedTimeCharges(self, report, order="date"):
        """locate all time charges associated with a given report confirmation code"""
        from ent.dom.Time import Time
        charges = self.db.fetchall(
            Time,
            where="id=ANY(SELECT charge from reported_times where report='%s')" % report,
            sort=order)
        
        return charges


    def retrieveTimeCharges(self, criteria, order):
        from ent.dom.Time import Time
        return self.db.fetchall(Time, where=criteria, sort=order)


    def retrieveOutstandingTimeCharges(self, username, order="date"):
        """locate all time charges marked 'n' by this user"""

        from ent.dom.Time import Time
        records = self.db.fetchall(
            Time,
            where="employee='%s' and status='n'" % username,
            sort=order)

        return records


    def retrieveExpenseReport(self, tag):
        """locate the expense report with the given id"""

        from ent.dom.ExpenseReport import ExpenseReport
        reports = self.db.fetchall(ExpenseReport, where="id='%s'" % tag)

        # there had better be only one
        return reports[0]


    def retrieveTimeChargeReport(self, tag):
        """locate the time charge report with the given id"""

        from ent.dom.TimeReport import TimeReport
        reports = self.db.fetchall(TimeReport, where="id='%s'" % tag)

        # there had better be only one
        return reports[0]


    def retrieveExpenseReports(self, criteria):
        """locate all the expense reports that match criteria"""

        from ent.dom.ExpenseReport import ExpenseReport
        reports = self.db.fetchall(
            ExpenseReport,
            where=criteria,
            sort="submitted")

        return reports


    def retrieveReimbursements(self, criteria):
        """locate all the reimbursements that match criteria"""

        from ent.dom.Reimbursement import Reimbursement
        reports = self.db.fetchall(
            Reimbursement,
            where=criteria,
            sort="submitted")

        return reports


    def retrieveInvoice(self, tag):
        """locate the invoice with the given id"""

        from ent.dom.Invoice import Invoice
        reports = self.db.fetchall(
            Invoice,
            where="id='%s'" % tag,
            sort="date")

        # there had better be only one
        return reports[0]


    def retrieveInvoices(self, criteria, sort=None):
        """locate all the invoices that match criteria"""

        if sort is None:
            sort = "date"

        from ent.dom.Invoice import Invoice
        reports = self.db.fetchall(
            Invoice,
            where=criteria,
            sort=sort)

        return reports


    def retrieveInvoicedItems(self, invoice):
        """locate all invoiced items associated with a given invoice id"""

        from ent.dom.InvoicedItem import InvoicedItem
        records = self.db.fetchall(
            InvoicedItem,
            where=("invoice='%s'" % invoice),
            )

        return records


    def retrieveInvoicedItem(self, tag):
        """locate an invoiced item given its id"""

        from ent.dom.InvoicedItem import InvoicedItem
        records = self.db.fetchall(
            InvoicedItem,
            where=("id='%s'" % tag)
            )

        # there had better only be one of these
        item = records[0]

        return item


    def retrieveAllExpenseReports(self, status=None, sortOrder=None):
        """locate all expense reports with a given status"""

        from ent.dom.ExpenseReport import ExpenseReport

        if not status:
            return self.db.fetchall(ExpenseReport, sort=sortOrder)

        return self.db.fetchall(ExpenseReport, where="status='%s'" % status, sort=sortOrder)


    def retrieveExpenseReportsByReimbursement(self, reimbursement, order="submitted"):
        """locate all expense reports associated with a given reimbursement confirmation code"""
        from ent.dom.ExpenseReport import ExpenseReport

        idSelector = "ANY(SELECT report from reimbursed_reports where reimbursement='%s')" % (
            reimbursement)

        reports = self.db.fetchall(
            ExpenseReport,
            where="id=%s" % idSelector,
            sort=order)
        
        return reports


    def retrieveReportReimbursment(self, tag):
        """locate the reimbursement that contains the given expense report"""

        from ent.dom.ReimbursedReport import ReimbursedReport

        records = self.db.fetchall(
            ReimbursedReport,
            where="report='%s'" % tag)

        if len(records) == 0:
            return None

        record = records[0]
        criteria = "id='%s'" % record.reimbursement
        reimbursements = self.retrieveReimbursements(criteria)

        return reimbursements[0]


    def retrieveTimeChargeReports(self, username):
        """locate all the expense reports submitted by a given user"""

        from ent.dom.TimeReport import TimeReport
        reports = self.db.fetchall(
            TimeReport,
            where="employee='%s'" % username,
            sort="submitted")

        return reports


    def retrieveAllTimeChargeReports(self, status=None, sortOrder=None):
        """locate all time charge reports with a given status"""

        from ent.dom.TimeReport import TimeReport

        if not status:
            return self.db.fetchall(TimeReport, sort=sortOrder)

        return self.db.fetchall(TimeReport, where="status='%s'" % status, sort=sortOrder)


    def retrieveUserGroups(self, username):
        """locate the groups to which the given user belongs"""

        from ent.dom.ACL import ACL
        records = self.db.fetchall(ACL, where="username='%s'" % username)

        groups = [ acl.groupname for acl in records ]

        return groups


    def retrievePaymentInstructions(self, office, currency):
        from ent.dom.PaymentInstructions import PaymentInstructions
        
        where = "status='a' and location='%s' and currency='%s'" % (office, currency)
        records = self.db.fetchall(PaymentInstructions, where=where)
        return records[0]


    def submitExpenseReport(self, confirmation, username, expenses):
        import time
        from ent.dom.Expense import Expense
        from ent.dom.ExpenseReport import ExpenseReport
        from ent.dom.ReportedExpense import ReportedExpense

        # create the expense report record
        report = ExpenseReport()
        report.status = 's'
        report.id = confirmation
        report.employee = username
        report.submitted = time.strftime("%Y/%m/%d")
        self.db.insertRow(report)

        # initialize the correlator table row
        association = ReportedExpense()
        association.report = confirmation

        # get the expenses
        for expense in expenses:
            # update the expense status
            where = "id='%s'" % expense
            assignments = [
                ("status", "s"),
                ]
            self.db.updateRow(Expense, assignments, where)

            # make an entry in the correlator table
            association.expense = expense
            self.db.insertRow(association)
            
        return


    def submitTimeChargeReport(self, confirmation, username):
        import time
        from ent.dom.Time import Time
        from ent.dom.TimeReport import TimeReport
        from ent.dom.ReportedTime import ReportedTime

        # create the timecharge record
        report = TimeReport()
        report.status = 's'
        report.id = confirmation
        report.employee = username
        report.submitted = time.strftime("%Y/%m/%d")
        self.db.insertRow(report)

        # initialize the correlator table row
        association = ReportedTime()
        association.report = confirmation

        # get the time charges
        charges = self.retrieveOutstandingTimeCharges(username)
        for charge in charges:
            
            # update the status
            where = "employee='%s' and status='n'" % username
            assignments = [
                ("status", "s"),
                ]
            self.db.updateRow(Time, assignments, where)

            # make an entry in the correlator table
            association.charge = charge.id
            self.db.insertRow(association)
            
        return


    def retireProject(self, tag):
        from ent.dom.Project import Project
        where = "id='%s'" % tag
        assignments = [
            ("status", "c"),
            ]
        self.db.updateRow(Project, assignments, where)
        return


    def __init__(self, name=None):
        if name is None:
            name = "clerk"
        super(Clerk, self).__init__(name, facility="clerk")

        return


# version
__id__ = "$Id: Clerk.py,v 1.15 2008-02-18 11:06:06 aivazis Exp $"

# End of file
