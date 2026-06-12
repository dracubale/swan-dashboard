const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,AlignmentType,LevelFormat,
TableOfContents,HeadingLevel,BorderStyle,WidthType,ShadingType,PageBreak}=require('docx');

const JADE="0F7B74", INK="1B1A16", SOFT="5C594E", GOLD="9A6B14", LINE="D9D2C4", TINT="F2F0E8", HEAD="E3F1EF";
const CW=9360;

// ---- helpers ----
const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,children:[new TextRun(t)]});
const H2=t=>new Paragraph({heading:HeadingLevel.HEADING_2,children:[new TextRun(t)]});
const H3=t=>new Paragraph({heading:HeadingLevel.HEADING_3,children:[new TextRun(t)]});
function runs(parts){ // parts: string | {t,b,i,c}
  if(typeof parts==='string') parts=[{t:parts}];
  return parts.map(p=> typeof p==='string'? new TextRun(p): new TextRun({text:p.t,bold:!!p.b,italics:!!p.i,color:p.c||undefined}));
}
const P=(parts,opt={})=>new Paragraph({spacing:{after:opt.after??120,before:opt.before??0},children:runs(parts)});
const lead=(label,rest)=>P([{t:label+': ',b:true},...(Array.isArray(rest)?rest:[{t:rest}])]);
function bullets(items){return items.map(it=>new Paragraph({numbering:{reference:"bul",level:0},spacing:{after:60},
  children: typeof it==='string'?runs(it):runs([{t:it.label+': ',b:true},{t:it.text}])}));}
function nums(items){return items.map(it=>new Paragraph({numbering:{reference:"num",level:0},spacing:{after:60},children:runs(it)}));}
const border={style:BorderStyle.SINGLE,size:1,color:LINE};
const borders={top:border,bottom:border,left:border,right:border};
function cell(text,w,opt={}){
  const kids=Array.isArray(text)?text.map(line=>new Paragraph({spacing:{after:20},children:runs(line)})):[new Paragraph({children:runs(text)})];
  return new TableCell({borders,width:{size:w,type:WidthType.DXA},shading:{fill:opt.fill||"FFFFFF",type:ShadingType.CLEAR},
    margins:{top:70,bottom:70,left:110,right:110},children:kids});
}
function hcell(text,w){return new TableCell({borders,width:{size:w,type:WidthType.DXA},shading:{fill:JADE,type:ShadingType.CLEAR},
  margins:{top:70,bottom:70,left:110,right:110},children:[new Paragraph({children:[new TextRun({text,bold:true,color:"FFFFFF"})]})]});}
// 3-col metric table: [name, def, objective]
function mtable(rows,headers){
  const ws=[2150,4010,3200];
  const head=new TableRow({tableHeader:true,children:headers.map((h,i)=>hcell(h,ws[i]))});
  const body=rows.map((r,ri)=>new TableRow({children:r.map((c,i)=>cell(c,ws[i],{fill:ri%2?TINT:"FFFFFF"}))}));
  return new Table({width:{size:CW,type:WidthType.DXA},columnWidths:ws,rows:[head,...body]});
}
// generic table with custom widths
function gtable(headers,rows,ws){
  const head=new TableRow({tableHeader:true,children:headers.map((h,i)=>hcell(h,ws[i]))});
  const body=rows.map((r,ri)=>new TableRow({children:r.map((c,i)=>cell(c,ws[i],{fill:ri%2?TINT:"FFFFFF"}))}));
  return new Table({width:{size:CW,type:WidthType.DXA},columnWidths:ws,rows:[head,...body]});
}
const gap=(h=120)=>new Paragraph({spacing:{after:h},children:[]});

const MH=["Chỉ số","Định nghĩa / Công thức","Mục tiêu — câu hỏi nó trả lời"];

// =================== CONTENT ===================
const children=[];
const push=(...x)=>x.forEach(e=>Array.isArray(e)?children.push(...e):children.push(e));

// Cover
push(new Paragraph({spacing:{before:1200,after:60},alignment:AlignmentType.LEFT,children:[new TextRun({text:"SWAN CLINIC",bold:true,size:30,color:JADE})]}));
push(new Paragraph({spacing:{after:240},children:[new TextRun({text:"Bảng điều khiển CEO — Tài liệu bàn giao & giải thích chỉ số",bold:true,size:40,color:INK})]}));
push(P([{t:"Phạm vi: ",b:true},"Mô tả từng trang, từng chỉ số, công thức tính và mục tiêu kinh doanh đằng sau. Dành cho chuyên gia phân tích."]));
push(P([{t:"Phiên bản dữ liệu ví dụ: ",b:true},"01/06–09/06/2026 (9 ngày). Các con số trong tài liệu chỉ là ảnh chụp minh hoạ; dashboard cập nhật hằng ngày."]));
push(P([{t:"Đơn vị tiền: ",b:true},"hiển thị rút gọn — tr = triệu VND, tỷ = tỷ VND, k = nghìn VND."]));
push(new Paragraph({children:[new PageBreakWrap()]}));

// (PageBreak helper)
function PageBreakWrap(){return new PageBreak();}

push(H1("Mục lục"));
push(new TableOfContents("Mục lục",{hyperlink:true,headingStyleRange:"1-2"}));
push(new Paragraph({children:[new PageBreak()]}));

// 1. Tổng quan hệ thống
push(H1("1. Tổng quan hệ thống & mục tiêu"));
push(P([{t:"Mục tiêu tổng thể. ",b:true},"Cung cấp cho CEO một bức tranh điều hành đầy đủ mỗi sáng (trước 6:00) mà không cần nhập liệu thủ công: hệ thống tự kéo dữ liệu doanh thu và quảng cáo, tự tính các chỉ số cấp CEO, và sinh một bản tin AI tóm tắt tình hình kèm hành động đề xuất."]));
push(lead("Nguồn dữ liệu",[{t:"(1) Google Sheet doanh thu mức bill (bill-level) của phòng khám; (2) Meta Ads API; (3) TikTok Ads API; (4) OpenAI để viết bản tin CEO."}]));
push(lead("Nhịp cập nhật","mỗi ngày ~5:45 sáng job chạy, ghi ra tệp data.json; dashboard nạp data.json và tự làm mới định kỳ. Bản tin AI sinh 1 lần mỗi sáng."));
push(lead("Triết lý thiết kế",[{t:"(a) tách bạch "},{t:"tiền thật (doanh thu hoàn tất)",b:true},{t:" với "},{t:"pipeline (cọc)",b:true},{t:"; (b) mọi chỉ số quy về "},{t:"mức bill",b:true},{t:" để nhất quán; (c) bản tin 3 tầng đọc: 30 giây / 3 phút / chuyên sâu."}]));
push(lead("7 trang","Tổng quan · Dịch vụ · Nền tảng (Meta vs TikTok) · Sale · Master · Bán chéo · Bản tin CEO."));

// 2. Khái niệm cốt lõi
push(H1("2. Khái niệm & quy ước cốt lõi (đọc trước)"));
push(P("Đây là các định nghĩa nền tảng mà mọi trang đều dựa vào. Hiểu đúng phần này thì đọc cả dashboard mới chính xác."));
push(H2("2.1 Mô hình mức bill (bill-level)"));
push(bullets([
 {label:"Gom theo số bill",text:"các dòng có cùng số bill (cột BILLL) thuộc về một bill/khách. Một bill có thể nhiều dòng (nhiều dịch vụ)."},
 {label:"Dòng đại diện (E=1)",text:"dòng có cột “Tính khách?” = 1 là dòng đại diện cho khách của bill đó (dùng để đếm khách, gán loại khách)."},
 {label:"Giá trị tiền",text:"cột GIÁ TRỊ BILL ghi theo nghìn VND, hệ thống nhân 1.000 để ra VND."},
]));
push(H2("2.2 Ba loại khách (phân loại tại dòng E=1 của mỗi bill)"));
push(mtable([
 ["Khách có doanh thu (DT)","Bill có thu tiền thật cho dịch vụ đã thực hiện (giá trị > 0, không phải cọc).","Đây là khách tạo doanh thu hoàn tất — thước đo “tiền thật”."],
 ["Khách cọc","Bill là tiền đặt cọc cho dịch vụ tương lai (nhận diện chữ “CỌC” ở cột NGƯỜI THỰC HIỆN).","Pipeline — tiền đã vào nhưng dịch vụ chưa thực hiện; KHÔNG tính là doanh thu hoàn tất."],
 ["Khách 0đ","Bill ghi nhận khách đến nhưng giá trị = 0 (tái khám, bảo hành, tư vấn không chốt…).","Đo lưu lượng khách không tạo doanh thu — nếu cao bất thường cần xem lại."],
],MH));
push(gap(60));
push(lead("Bill “mixed”",[{t:"bill vừa có dịch vụ thu tiền (dòng chính) vừa có cọc cho dịch vụ tương lai (dòng phụ). Hệ thống tính bill này là "},{t:"khách có doanh thu",b:true},{t:" (vì có tiền thật) và gắn cờ riêng — không đếm trùng thành khách cọc."}]));
push(H2("2.3 Ba thước đo tiền — tách bạch"));
push(mtable([
 ["Doanh thu hoàn tất","Tổng giá trị các bill khách có DT (dịch vụ đã thực hiện, đã thu tiền). KHÔNG gồm cọc.","“Tiền thật” đã ghi nhận trong kỳ — chỉ số doanh thu chính."],
 ["Cọc / pipeline","Tổng tiền đặt cọc trong kỳ.","Tiền cam kết cho tương lai; theo dõi để biết lượng việc sắp tới."],
 ["Tổng cash-in","Doanh thu hoàn tất + cọc.","Tổng tiền thực thu vào phòng khám trong kỳ (khớp với “Doanh số” trên sheet)."],
],MH));
push(H2("2.4 Phân nhóm dịch vụ"));
push(P([{t:"Mọi dịch vụ được quy về "},{t:"8 nhóm chính",b:true},{t:": Tiêm, Máy, Căng chỉ, Mũi, Ngực, Mí/Mắt, Mông, Hút mỡ (qua hàm phân loại, bỏ dấu để khớp). Dịch vụ không khớp gom vào “(chưa rõ DV)”. Quảng cáo được gán nhóm qua thẻ [TÊN DV] trong tên chiến dịch/ad."}]));
push(H2("2.5 Khung thời gian"));
push(mtable([
 ["Hôm nay","Ngày hệ thống hiện tại — đang chạy dở (quảng cáo mới tới giờ hiện tại).","Theo dõi vận hành trong ngày; lưu ý chưa trọn ngày."],
 ["Ngày đã chốt","Các ngày trước hôm nay (đã trọn ngày).","Dùng làm nền so sánh đáng tin (không lẫn ngày dở dang)."],
 ["MTD (tháng đến nay)","Tất cả ngày trong tháng tính đến hôm nay, GỒM hôm nay.","Số luỹ kế “tháng này tới giờ”. Đây là số lớn (headline) ở các thẻ KPI."],
 ["3 / 7 / 15 / 30 ngày","N ngày đã chốt gần nhất (không gồm hôm nay).","So sánh ngắn/trung hạn; “30 ngày” khác MTD ở chỗ không gồm hôm nay."],
],["Khung","Định nghĩa","Mục tiêu"]));

// 3. Quy ước màu
push(H1("3. Quy ước màu sắc & trực quan"));
push(mtable([
 ["Màu tốt/xấu","Xanh = tốt hơn nền · Vàng = lệch nhẹ · Đỏ = lệch mạnh. Tô theo BẢN CHẤT của chỉ số (g=+1 cao là tốt, g=−1 thấp là tốt, g=0 trung tính), không theo lên/xuống đơn thuần.","Ví dụ: chi phí giảm → xanh (tốt); doanh thu giảm → đỏ (xấu)."],
 ["Sparkline","Đường xu hướng nhỏ trong thẻ/bảng, lấy tối đa 30 ngày đã chốt gần nhất; màu theo bản chất + xu hướng; rê chuột hiện khoảng ngày.","Thấy ngay hình dạng xu hướng bên cạnh con số."],
 ["Heatmap (thang màu)","Trong bảng so sánh, ô tô nền xanh đậm/nhạt theo giá trị (đậm = cao).","Quét nhanh ai/nhóm nào cao–thấp."],
 ["Light / Dark","Có nút chuyển giao diện sáng/tối, tự nhớ lựa chọn.","Đọc thoải mái trên mọi điều kiện màn hình."],
],["Yếu tố","Cách hoạt động","Mục tiêu"]));

// 4. Từng trang
push(new Paragraph({children:[new PageBreak()]}));
push(H1("4. Mô tả từng trang & chỉ số"));

// 4.1 Overview
push(H2("4.1 Trang “Tổng quan”"));
push(lead("Mục tiêu trang","một màn hình cho buổi sáng — trả lời nhanh: kênh nào đang nghẽn, doanh thu tháng tới đâu, các chỉ số cốt lõi và xu hướng."));
push(H3("Thanh trạng thái dữ liệu"));
push(P("Cho biết dữ liệu cập nhật tới ngày nào, giờ sinh dữ liệu, và lần kiểm tra gần nhất. Đỏ nếu dữ liệu cũ (stale)."));
push(H3("3 cửa quyết định (phễu)"));
push(P([{t:"Trả lời: tiền đang nghẽn ở “cửa” nào trong hành trình "},{t:"Quảng cáo → Tin nhắn → Khách → Giá trị",b:true},{t:". Chọn được khung thời gian (mặc định Hôm nay)."}]));
push(mtable([
 ["Cửa 1 — Quảng cáo → Tin nhắn","Số tin nhắn (lead) tạo ra; kèm CPL/tin nhắn = chi quảng cáo ÷ số tin nhắn, và chia theo Meta/TikTok, theo nhóm dịch vụ.","Tiền quảng cáo có tạo ra đủ lead với giá rẻ không?"],
 ["Cửa 2 — Tin nhắn → Khách","% chuyển đổi = (khách DT + cọc) ÷ tin nhắn; số khách DT, khách cọc, khách thăm khám; chi phí ad/khách.","Sale có chốt được lead thành khách không?"],
 ["Cửa 3 — Khách → Giá trị","ROAS, AOV, bill trung vị, tỉ lệ & giá trị bán chéo.","Mỗi khách mang về bao nhiêu giá trị?"],
],MH));
push(P([{t:"Cách dùng: ",b:true},"Cửa 1 yếu → sửa quảng cáo. Cửa 1 ổn, Cửa 2 yếu → khâu chốt sale. Cửa 1–2 ổn, Cửa 3 yếu → khách giá trị thấp / thiếu bán chéo."]));
push(H3("Trạng thái doanh thu (tháng này)"));
push(P("Ba ô tách bạch: Doanh thu hoàn tất · Cọc/pipeline · Tổng cash-in (xem mục 2.3). Ví dụ kỳ 01–09/06: hoàn tất 3,54 tỷ · cọc 64 tr · cash-in 3,61 tỷ."));
push(H3("6 thẻ KPI chính"));
push(P([{t:"Mỗi thẻ: số lớn = "},{t:"MTD (/tháng)",b:true},{t:"; có sparkline 30 ngày; và các dòng phụ Hôm nay / Hôm qua / 7 ngày / 30 ngày để so sánh."}]));
push(mtable([
 ["Doanh thu","Tổng bill khách đã thu, không gồm cọc.","Tiền thật của tháng đang ở mức nào?"],
 ["Chi phí quảng cáo","Tổng chi Meta + TikTok.","Đang tiêu bao nhiêu cho quảng cáo? (bản chất trung tính — không tự nó tốt/xấu)."],
 ["ROAS","Doanh thu ÷ chi quảng cáo.","Một đồng quảng cáo đổi lại bao nhiêu đồng doanh thu?"],
 ["Khách có doanh thu","Số khách trả tiền thật (chưa gồm cọc).","Bao nhiêu khách tạo doanh thu trong tháng?"],
 ["Chi phí ad / khách (CAC)","Chi quảng cáo ÷ (khách DT + cọc).","Giá vốn quảng cáo để có một khách đã chốt là bao nhiêu?"],
 ["Chi phí ad / DS","Chi quảng cáo ÷ doanh thu.","Quảng cáo chiếm bao nhiêu % doanh thu? (thấp là tốt)."],
],MH));
push(gap(60));
push(P([{t:"Lưu ý CAC: ",b:true},"mẫu số dùng (khách DT + cọc) vì cả khách cọc cũng tốn chi phí quảng cáo để có được; còn thẻ “Khách có doanh thu” chỉ đếm khách trả tiền thật."]));
push(H3("Biểu đồ “Doanh thu & hiệu quả theo ngày”"));
push(P("Cột = doanh thu thuần (và cọc) mỗi ngày; đường = bill trung vị; điểm = ROAS mỗi ngày (trục phải). Chọn khung thời gian; rê/chạm từng ngày để xem chi tiết."));
push(H3("4 thẻ phụ"));
push(mtable([
 ["Bill trung vị","Giá trị giữa của các bill khách (median).","Một bill “điển hình” đáng giá bao nhiêu? (ít bị kéo lệch bởi bill khủng)."],
 ["Bill trung bình (AOV)","Doanh thu ÷ số khách có DT.","Giá trị đơn trung bình."],
 ["Tin nhắn","Tổng lead Meta + TikTok.","Lưu lượng lead đầu phễu."],
 ["Tỉ lệ chuyển đổi","Msg → khách (DT + cọc): (khách DT + cọc) ÷ tin nhắn.","Tỉ lệ biến lead thành khách đã chốt."],
],MH));
push(H3("Khách mới / Tái khám & Cờ chất lượng dữ liệu"));
push(P("Tách New (khách mới) vs TK (tái khám). Các “cờ” cảnh báo chất lượng dữ liệu (vd “3 bill thiếu dòng E=1”, “bill vừa có DT vừa có cọc”, “map doanh thu → DV %”) giúp biết độ tin cậy của số."));

// 4.2 Service
push(new Paragraph({children:[new PageBreak()]}));
push(H2("4.2 Trang “Dịch vụ”"));
push(lead("Mục tiêu trang","hiểu cơ cấu doanh thu theo nhóm dịch vụ và mức độ phụ thuộc/ổn định của từng nhóm."));
push(mtable([
 ["Cơ cấu doanh thu (donut)","% doanh thu hoàn tất theo từng nhóm dịch vụ.","Nhóm nào đang gánh doanh thu?"],
 ["Số lượt có doanh thu","Số lần dịch vụ được làm và thu tiền (loại 0đ và cọc).","Tần suất sử dụng dịch vụ."],
 ["Doanh thu (có heatmap)","Tổng doanh thu hoàn tất của nhóm.","Quy mô tiền của nhóm."],
 ["Trung vị / P90","Giá trị giữa / ngưỡng 10% lượt đắt nhất.","Một lượt điển hình & nhóm khách cao cấp đáng giá bao nhiêu."],
 ["CV (độ phân tán)","Độ lệch giá trị giữa các lượt (≥140% là rất lệch).","Doanh thu nhóm có ổn định hay phụ thuộc vài ca lớn?"],
 ["Top 20%","20% lượt giá trị cao nhất gánh bao nhiêu % doanh thu nhóm.","Mức tập trung — rủi ro phụ thuộc số ít khách."],
 ["Tỉ lệ mua kèm theo dịch vụ","Trong khách dùng nhóm này, bao nhiêu % làm thêm nhóm khác cùng lần đến.","Nhóm nào kéo theo bán chéo tốt."],
],MH));

// 4.3 Platform
push(H2("4.3 Trang “Nền tảng” (Meta vs TikTok)"));
push(lead("Mục tiêu trang","so sánh hiệu quả 2 nền tảng quảng cáo và từng ad để quyết định scale/cắt ngân sách."));
push(mtable([
 ["Bảng so sánh nền tảng","Chi, % chi, hội thoại, lead mới, CPL hội thoại, CPL lead, CPM, CTR, frequency cho Meta vs TikTok.","Nền tảng nào rẻ/hiệu quả hơn ở từng khâu?"],
 ["Nền tảng × Dịch vụ","Chi & lead chia theo nhóm dịch vụ trên mỗi nền tảng.","Nền tảng nào hợp dịch vụ nào?"],
 ["Bảng từng ad + trạng thái","Mỗi ad: chi, lead, CPL, nhãn Scale / Giữ / Watch / Cut / Hold; mức tập trung “ad thắng”; chi lãng phí (ad chi nhiều ít/không ra lead).","Ad nào nên tăng tiền, ad nào nên cắt?"],
 ["Proxy ROAS","Ước lượng ROAS bằng cách ghép quảng cáo với doanh thu theo NHÓM dịch vụ (tương quan, không phải khớp từng khách).","Gợi ý hiệu quả tương đối — KHÔNG dùng để kết luận attribution thật."],
],MH));
push(gap(60));
push(P([{t:"Cảnh báo quan trọng: ",b:true},"Proxy ROAS chưa phải ROAS thật. Đừng scale ngân sách chỉ dựa vào proxy. Lưu ý không cộng “new contacts” của Meta với “conversations” của TikTok — khác khái niệm."]));

// 4.4 Sale
push(new Paragraph({children:[new PageBreak()]}));
push(H2("4.4 Trang “Sale” (telesale — gọi điện chốt khách trước khi đến)"));
push(lead("Mục tiêu trang","đo hiệu quả từng nhân viên telesale, tách giữa “mang nhiều tiền” và “chốt khéo”."));
push(H3("Ranking doanh thu"));
push(mtable([
 ["Khách DT / ngày","Số khách có doanh thu của sale ÷ số ngày đã qua trong tháng. (có heatmap)","CHỈ SỐ NĂNG SUẤT CHÍNH để đo sale — chuẩn hoá theo ngày, không thiên vị người làm nhiều/ít ngày."],
 ["DT hoàn tất / Cọc / Cash-in","Doanh thu của sale theo 3 thước đo tiền. (DT có heatmap)","Ai mang về nhiều tiền nhất?"],
 ["AOV / Trung vị","Giá trị đơn trung bình / điển hình của sale.","Sale phục vụ khách giá trị cao hay thấp?"],
 ["New / TK","Số khách mới / tái khám.","Cơ cấu nguồn khách của sale."],
],MH));
push(H3("Ranking chất lượng chuyển đổi"));
push(mtable([
 ["% trả tiền","Khách tạo doanh thu ÷ tổng khách của sale.","Chốt ra tiền tốt đến đâu?"],
 ["% có giá trị TM","(Khách DT + cọc) ÷ tổng khách.","Tỉ lệ khách tạo ra giá trị thương mại (kể cả cọc)."],
 ["% cọc / % 0đ","Tỉ lệ khách cọc / khách 0đ.","Bao nhiêu chỉ đặt cọc, bao nhiêu không ra tiền."],
 ["New / TK chốt","Số khách mới / tái khám đã trả tiền.","Chốt khách mới hay sống nhờ tái khám?"],
],MH));
push(P([{t:"Vì sao tách 2 bảng: ",b:true},"doanh thu cao chưa chắc chốt giỏi — có thể do được chia khách giá trị cao. Bảng chất lượng tách riêng kỹ năng chốt."]));
push(P([{t:"Hạn chế: ",b:true},"mỗi bill gán cho người trực tiếp chốt. Để có phễu đầy đủ (lead → booking → show-up → chốt) cần thêm dữ liệu phân bổ lead từ CRM/Messenger."]));

// 4.5 Master
push(H2("4.5 Trang “Master” (trợ lý bác sĩ — chốt dịch vụ khi khách đến)"));
push(lead("Mục tiêu trang","đánh giá master công bằng — master nhận nhiều khách giá trị cao thì doanh thu tự nhiên cao, nên cần chuẩn hoá."));
push(mtable([
 ["Ranking doanh thu","DT / cọc / AOV / trung vị / P90 / New-TK của master. (DT có heatmap)","Master nào tạo nhiều doanh thu?"],
 ["Value Index","DT thực tế ÷ DT kỳ vọng. Kỳ vọng = cộng AOV trung bình toàn clinic của nhóm dịch vụ chính mà mỗi khách của master đó nhận. ≥1,1 khai thác tốt hơn mặt bằng · 0,9–1,1 bình thường · <0,9 nên coaching.","Master KHAI THÁC giá trị khách tốt hơn hay kém mặt bằng chung? (loại bỏ lợi thế được chia khách dễ)."],
 ["Bán chéo theo master","Tỉ lệ & uplift bán chéo.","Master nào kéo thêm dịch vụ tốt?"],
 ["Cảnh báo","Master có % khách 0đ cao hoặc Value Index thấp.","Ai cần coaching / cân nhắc lại cách giao khách."],
],MH));
push(P([{t:"Ví dụ Value Index: ",b:true},"NGỌC 1,41 (khai thác tốt) · GIANG 0,7 (dưới kỳ vọng, nên coaching)."]));

// 4.6 Cross-sell
push(new Paragraph({children:[new PageBreak()]}));
push(H2("4.6 Trang “Bán chéo” (Cross-sell)"));
push(lead("Mục tiêu trang","đo và khai thác cơ hội bán thêm dịch vụ trong cùng lần khách đến."));
push(mtable([
 ["Tỉ lệ mua kèm (attach rate)","% khách có doanh thu làm ≥2 nhóm dịch vụ trong cùng lần đến.","Mức độ bán chéo hiện tại."],
 ["Ma trận cặp dịch vụ","Cặp nhóm hay đi cùng nhau (vd Tiêm ↔ Máy) và giá trị/số bill.","Gợi ý combo nên đẩy."],
 ["Attach theo Sale / Master","Tỉ lệ bán chéo theo từng người.","Ai bán chéo giỏi để nhân rộng cách làm."],
 ["Máy tính cơ hội","Mô phỏng nếu tăng attach +5/+10/+15 điểm % thì doanh thu tăng thêm bao nhiêu.","Định lượng cơ hội để đặt mục tiêu."],
],MH));
push(P([{t:"Lưu ý định nghĩa: ",b:true},"dashboard tính attach theo 8 nhóm chính (~8,8%); sheet nội bộ tính ~11,83% theo một định nghĩa “sub-item” chưa được xác nhận. Hai cách định nghĩa khác nhau — cần thống nhất. Để đo uplift bán chéo trực tiếp chính xác hơn, nên nhập giá trị thật cho các dòng dịch vụ phụ đang để 0đ."]));

// 4.7 Memo
push(H2("4.7 Trang “Bản tin CEO” (bản tin hằng ngày)"));
push(lead("Mục tiêu trang","đọc nhanh “hôm qua thế nào & hôm nay cần làm gì”. Bản tin do AI (OpenAI) viết khi vận hành thật."));
push(P([{t:"Cấu trúc 3 tầng đọc:",b:true}]));
push(bullets([
 {label:"Tầng 30 giây",text:"Tóm tắt điều hành · Cảnh báo & bất thường (theo luật: doanh thu tụt, chi tăng mà doanh thu không tăng, CPL/ROAS lệch mạnh, khách 0đ tăng, dữ liệu cũ…) · Hành động hôm nay (P1/P2 kèm người phụ trách, lý do, tác động)."},
 {label:"Tầng 3 phút",text:"Nhịp tim kinh doanh (bảng 14 chỉ số), Thay đổi đáng kể, Quảng cáo & nền tảng, Doanh thu theo dịch vụ, Sale & Master nổi bật, Bán chéo."},
 {label:"Liên kết",text:"mỗi khối có nút bấm nhảy tới trang chi tiết tương ứng."},
]));
push(H3("Bảng “Nhịp tim kinh doanh”"));
push(P("14 chỉ số cốt lõi, mỗi dòng so sánh: Hôm qua · vs hôm trước · vs 3 ngày · vs 7 ngày · MTD (in đậm) · cột Xu hướng (sparkline). Màu xanh/vàng/đỏ theo bản chất chỉ số."));
push(P([{t:"Cơ sở so sánh: ",b:true},"“hôm qua” = ngày đã chốt gần nhất; nền so sánh tính trên các ngày đã chốt. So với nền 7 ngày đáng tin hơn so với hôm trước (đỡ nhiễu)."]));
push(P([{t:"Chỉ số sale chính trong bản tin: ",b:true},"“Năng suất khách DT/ngày” được đặt lên đầu khối Sale — đây là thước đo quan trọng nhất để đánh giá telesale."]));

// 5. Bảng công thức tổng hợp
push(new Paragraph({children:[new PageBreak()]}));
push(H1("5. Bảng tra công thức nhanh"));
push(gtable(["Chỉ số","Công thức"],[
 ["Doanh thu hoàn tất","Σ giá trị bill khách có DT (không gồm cọc)"],
 ["Cash-in","Doanh thu hoàn tất + cọc"],
 ["ROAS","Doanh thu hoàn tất ÷ chi quảng cáo"],
 ["Chi phí ad / khách (CAC)","Chi quảng cáo ÷ (khách DT + cọc)"],
 ["Chi phí ad / DS","Chi quảng cáo ÷ doanh thu hoàn tất"],
 ["AOV (bill trung bình)","Doanh thu hoàn tất ÷ số khách có DT"],
 ["Bill trung vị","Median của giá trị các bill khách có DT"],
 ["Tỉ lệ chuyển đổi","(Khách DT + khách cọc) ÷ số tin nhắn"],
 ["CPL / tin nhắn","Chi quảng cáo ÷ số tin nhắn"],
 ["Attach rate","Khách làm ≥2 nhóm DV cùng lần ÷ khách có DT"],
 ["Khách DT / ngày (sale)","Khách có DT của sale ÷ số ngày đã qua trong tháng"],
 ["Value Index (master)","DT thực tế ÷ DT kỳ vọng (Σ AOV-toàn-clinic theo nhóm chính của khách master đó)"],
 ["CV (dịch vụ)","Độ lệch chuẩn ÷ trung bình giá trị các lượt của nhóm"],
],[3400,5960]));

// 6. Cảnh báo & hạn chế
push(H1("6. Cảnh báo & hạn chế cần biết khi phân tích"));
push(bullets([
 {label:"Proxy ROAS ở trang Nền tảng",text:"là tương quan theo nhóm dịch vụ, KHÔNG phải attribution khớp từng khách. Cần nguồn lead / campaign-id / SĐT khách để có ROAS nền tảng thật."},
 {label:"Đếm bill khách lệch ±2",text:"do một số bill thiếu dòng E=1 (lỗi nhập liệu). Không ảnh hưởng số tiền (doanh thu vẫn khớp tuyệt đối với sheet)."},
 {label:"Bán chéo trực tiếp",text:"để đo uplift chính xác cần nhập giá trị thật cho các dòng dịch vụ phụ hiện để 0đ."},
 {label:"Phễu sale đầy đủ",text:"hiện chưa có lead → booking → show-up; cần dữ liệu CRM/Messenger."},
 {label:"Sparkline còn ngắn",text:"hiển thị tối đa 30 ngày đã chốt; hiện mới ~8 ngày nên xu hướng chưa “đã”."},
 {label:"“Hôm nay” đang chạy dở",text:"quảng cáo chỉ tới giờ hiện tại; vì vậy các so sánh nền dùng ngày đã chốt."},
 {label:"Định nghĩa attach chưa thống nhất",text:"8,8% (8 nhóm) vs ~11,83% (sheet, sub-item) — cần chốt định nghĩa."},
]));

// 7. Pipeline
push(H1("7. Nguồn dữ liệu & luồng cập nhật"));
push(nums([
 "Job chạy mỗi sáng (~5:45) trên môi trường máy chủ luôn bật.",
 "Kéo: doanh thu từ Google Sheet (bill-level) + quảng cáo từ Meta Ads API & TikTok Ads API.",
 "Chạy bộ trích xuất (logic mức bill, phân loại khách/cọc/0đ, gom nhóm dịch vụ) → tính chỉ số → ghi data.json.",
 "Sinh bản tin CEO bằng OpenAI (1 lần/sáng).",
 "Dashboard (HTML tĩnh) nạp data.json và tự làm mới định kỳ; song ngữ Việt/Anh tối giản, có light/dark.",
]));
push(gap(120));
push(P([{t:"Hết tài liệu. ",b:true},"Mọi định nghĩa trên phản ánh logic đang chạy của dashboard; khi đổi quy ước (vd thống nhất định nghĩa attach, hoặc đổi “khách có doanh thu” thành “khách đã chốt = DT+cọc”) cần cập nhật cả tài liệu này."]));

// ---- build ----
const doc=new Document({
  styles:{default:{document:{run:{font:"Arial",size:21,color:INK}}},
    paragraphStyles:[
      {id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:30,bold:true,font:"Arial",color:JADE},paragraph:{spacing:{before:300,after:160},outlineLevel:0}},
      {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:25,bold:true,font:"Arial",color:INK},paragraph:{spacing:{before:220,after:120},outlineLevel:1}},
      {id:"Heading3",name:"Heading 3",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:22,bold:true,font:"Arial",color:SOFT},paragraph:{spacing:{before:140,after:80},outlineLevel:2}},
    ]},
  numbering:{config:[
    {reference:"bul",levels:[{level:0,format:LevelFormat.BULLET,text:"•",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:280}}}}]},
    {reference:"num",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:300}}}}]},
  ]},
  sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:1440,right:1440,bottom:1440,left:1440}}},children}]
});
Packer.toBuffer(doc).then(buf=>{fs.writeFileSync("/mnt/user-data/outputs/Swan_Dashboard_Handover_Full.docx",buf);console.log("written",buf.length);});
