      #inserts titles for all each contributor
        # def insert_title(owl_id,row_id):
        #     title_data = [owl_id, f"=VLOOKUP(A{row_id},'Owl ID reference'!$A$2:$B$600,2,FALSE)", 'Contribution', 'Has this contribution been discussed with your WGL?','Link to Work', 'Other notes', 'Time contributed (Hours)', '# Functional area', 'Nominated WGL to review' ,'Product',
        #     f'=sumifs($K$3:$K$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"F.Nest")', f'=sumifs($L$3:$L$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Product")', f'=sumifs(M$3:M$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"BD")',
        #     f'=sumifs($N$3:$N$1000,$B$3:B$1000,B{row_id},$H$3:$H$1000,"Creative & Design")', f'=sumifs($O$3:$O$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Dev/Engineering")', f'=sumifs($P$3:$P$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Growth&Marketing")',
        #     f'=sumifs($Q$3:$Q$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Expenses")', f'=sumifs($R$3:$R$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"MVI")', f'=sumifs($S$3:$S$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Analytics")',
        #     f'=sumifs($T$3:$T$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Institutional Business")', f'=sumifs($U$3:$U$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Talent, Ops & Change")', f'=sumifs($V$3:$V$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"MetaGov")',
        #     f'=sumifs($W$3:$W$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Other")', f'=sumifs($X$3:$X$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Lang-Ops")',f'=sumifs($Y$3:$Y$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Asia Pacific")',
        #     f'=sumifs($Z$3:$Z$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Woman+Non-Binary")', f'=sumifs($AA$3:$AA$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Governance")', f'=sum(K{row_id}:AA{row_id})+AC{row_id + 1}', '', '', '',f'=(AB{row_id}/$B$1)+AD{row_id + 1}',
        #     f'=AE{row_id + 1}']

        #     ## WXY AC fixed USDC Stipen
        #     #need to fix data array and update 

        #     self.raw_input.insert_row(title_data, index = row_id, value_input_option='USER_ENTERED')


            #Format the first A-B Cells
            # self.raw_input.format(f'A{row_id}:B{row_id}', {
            #     "backgroundColor": {
            #     "red": 1.0,
            #     "green": 0.0,
            #     "blue": 0.0
            #     },
            #     "horizontalAlignment": "CENTER",
            #     "textFormat": {
            #     "foregroundColor": {
            #         "red": 1.0,
            #         "green": 1.0,
            #         "blue": 1.0
            #     },
            #     "fontSize": 12,
            #     "bold": True
            #     }
            # })
            # #Format for C-H cells
            # self.raw_input.format(f'C{row_id}:J{row_id}', {
            #         "backgroundColor": {
            #         "red": 0.15,
            #         "green": 0.0,
            #         "blue": 0.50
            #         },
            #         "horizontalAlignment": "CENTER",
            #         "textFormat": {
            #         "foregroundColor": {
            #             "red": 1.0,
            #             "green": 1.0,
            #             "blue": 1.0
            #         },
            #         "fontSize": 12,
            #         "bold": True
            #         }
            # }) 
            # #Format for I-Z cells
            # self.raw_input.format(f'K{row_id}:AH{row_id}', {
            #     "backgroundColor": {
            #     "red": 0.15,
            #     "green": 0.0,
            #     "blue": 0.50
            #     },
            #     "horizontalAlignment": "CENTER",
            #     "textFormat": {
            #     "foregroundColor": {
            #         "red": 1.0,
            #         "green": 1.0,
            #         "blue": 1.0
            #     },
            #     "fontSize": 10,
            #     "bold": False
            #     }
            # })