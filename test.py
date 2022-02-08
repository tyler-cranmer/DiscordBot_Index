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

newlist = [['#032', 'mel.eth', 'Contribution INFO', 'Yes', 'Link to work', 'Other Notes', 'Time contributed (Hours)', 'Community', 'Sustainability', 'Elliott'], ['#032', 'mel.eth', 'Contribution INFO10', 'Yes', '---', '---', 'Time contributed (Hours)', 'Product', 'Automated Pod', 't'], ['#032', 'mel.eth', 'Contribution INFO2', 'Yes', 'Link to work2', 'Other Notes2', 'Time contributed (Hours)', 'Growth', 'Accountability', 'Elliott'], ['#032', 'mel.eth', 'Contribution INFO3', 'Yes', 'Link to work3', 'Other Notes3', 'Time contributed (Hours)', 'Governance', 'Operational Funding & Payroll', 'ELLIOT'], ['#032', 'mel.eth', 'Contribution INFO4', 'Yes', 'Link to work4', 'Other Notes4', 'Time contributed (Hours)', 'Finance', 'Investment Pod', 'ELLIOT'], ['#032', 'mel.eth', 'Contribution INFO5', 'Yes', 'Link to work5', 'Other Notes5', 'Time contributed (Hours)', 'Product', 'Tokenomics', 'ELLIOT'], ['#032', 'mel.eth', 'Contribution INFO6', 'No', '---', '---', 'Time contributed (Hours)', 'Community', 'Content', 'f'], ['#032', 'mel.eth', 'Contribution INFO7', 'No', '---', '---', 'Time contributed (Hours)', 'Growth', 'Visual & Design', 'p'], ['#032', 'mel.eth', 'Contribution INFO8', 'Yes', '---', '---', 'Time contributed (Hours)', 'Governance', 'Visual & Design', 'f'], ['#032', 'mel.eth', 'Contribution INFO9', 'No', '---', '---', 'Time contributed (Hours)', 'Finance', 'Growth Grants Program', 'g']]
finance_list = []
growth_list = []
community_list = []
product_list = []
governance_list = []
other_list = []
for x in range(len(newlist)):
  if newlist[x][7] == 'Finance':
    finance_list.append(newlist[x])
  elif newlist[x][7] == 'Growth':
    growth_list.append(newlist[x])
  elif newlist[x][7] == 'Governance':
    governance_list.append(newlist[x])
  elif newlist[x][7] == 'Community':
    community_list.append(newlist[x])
  else:
    product_list.append(newlist[x])  

print(f'finance: {finance_list} \n')
print(f'Community: {community_list} \n')
print(f'Growth: {growth_list} \n')
print(f'Governance: {governance_list} \n')
print(f'Poduct: {product_list} \n')