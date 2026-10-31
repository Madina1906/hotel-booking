# P03 dizayn eslatmalari

## Nima uchun koddan oldin dizayn qilish kerak
Past darajadagi dizayn qaysi sinflar bo'lishini (Guest, Room, Reservation, DateRange...), ularning har biri qanday ma'lumotni saqlashini, qanday ishlarni bajarishini va qaysi sinf qaysi birini chaqirishini hal qiladi. Shunda har bir qoida (masalan, "ikki mehmon bir kechada bitta xonani ololmaydi") faqat bitta joyda, DateRange.Overlaps() da yoziladi va o'zgartirish kerak bo'lsa, bir joyni o'zgartirish kifoya.

## Metodlar qayerda joylashgan
- **Cancel()** Reservation sinfida joylashgan, chunki bekor qilish bronning o'z holatini (Confirmed → Cancelled) o'zgartiradi va bu holatni faqat bronning o'zi biladi. Hech narsa o'chirilmaydi, shuning uchun tarix saqlanib qoladi.
- **HasOverlap(room, stay)** ReservationStore sinfida joylashgan, chunki barcha bronlar ro'yxatini faqat do'kon ko'ra oladi. Har bir bronning "bu xonani bloklaydimi?" degan savoliga (Blocks) do'kon o'zi javob yig'adi.

## Faoliyat izlari
Barcha izlar Maya R7 ni 12–14 noyabrga band qilgan holat uchun.

**Omar, R7, 13–15 noyabr**
1. "Chiqish ro'yxatdan o'tgandan keyinmi?" → Ha (15 > 13).
2. "Tasdiqlangan bron bir kechani ulashadimi?" → Ha (13-kecha Mayaniki).
3. So'rov "Unavailable" bilan tugaydi, hech narsa saqlanmaydi.

**Nora, R7, 14–16 noyabr**
1. "Chiqish ro'yxatdan o'tgandan keyinmi?" → Ha (16 > 14).
2. "Tasdiqlangan bron bir kechani ulashadimi?" → Yo'q (Maya 14-kuni chiqib ketadi, 14-kecha bo'sh).
3. Bron Confirmed holatida saqlanadi, tasdiqlash xati yuboriladi, "Accepted R102" qaytadi.

**Omar, R8, 15–15 noyabr**
1. "Chiqish ro'yxatdan o'tgandan keyinmi?" → Yo'q (15 > 15 noto'g'ri).
2. So'rov birinchi rombdayoq "InvalidDates" bilan tugaydi. Ikkinchi savolga yetib ham bormaydi, hech narsa saqlanmaydi.

## Prediction
Nora uchun R7, 14–16 noyabr so'rovida "Accepted R102" qatorini kutaman: Maya 14-kuni chiqib ketadi, shuning uchun umumiy kecha yo'q, bron qabul qilinadi va u ikkinchi bron bo'lgani uchun id R102 bo'ladi.

## Race
**Bashorat:** Maya va Omar 12–14 noyabr kunlari R7 ni bir vaqtda bron qilsa, R7 da 1 ta tasdiqlangan bron bo'lishi kerak deb o'ylagandim, lekin kod himoyalanmagani uchun 2 ta bo'ladi deb kutaman.

**Natija:** Ikkala mehmon ham "Accepted" oldi (R101 va R102) va R7 da bir xil kechalar uchun 2 ta tasdiqlangan bron paydo bo'ldi, ya'ni R3 talabi buzildi.
**Sabab:** Muammo Reserve ichidagi `HasOverlap()` (tekshirish) va `Save()` (saqlash) chaqiruvlari orasida paydo bo'ladi: ikkala so'rov ham saqlashdan oldin tekshirib bo'sh javob oldi, keyin har biri eskirgan javobga ishonib saqladi.

# P04 dizayn yozuvlari

## Refactoring
Refaktoring degani kodni qayta tartibga solish: fayllarni bo'lish, nomlarni to'g'rilash, sinflar bir-biriga qanday bog'lanishini o'zgartirish. Lekin ilova mehmon uchun nima qilsa, aynan o'shani qilishda davom etishi shart: javoblar, raqamlar va natijalar o'zgarmaydi. Mehmonxona foyesidagi mebelni boshqacha qo'yish kabi: xona boshqacha ko'rinadi, lekin mehmonlar baribir bir xil natija bilan ro'yxatdan o'tadi.

Must stay the same:
- 2-qadamdagi 6 ta test: har bir kichik o'zgarishdan keyin ham yashil bo'lib qolishi kerak.
- Demo chiqishi: P03 dagidek aynan to'qqiz qator, bitta so'z ham o'zgarmasligi kerak.
- Poyga demosi: hali ham "Double booking!" chiqishi kerak. Poygani tuzatish xatti-harakatni o'zgartiradi, shuning uchun u refaktoring emas, bu P09 ning ishi.

## What our code breaks
- BookingService asks for exactly ReservationStore (D: dependency inversion).
  In P07 we would have to edit BookingService just to use a database.
- BookingService konstruktori aynan EmailSender sinfini so'raydi (D va O tamoyillari). Mehmonxona SMS tasdiqlarini ham xohlasa, ishlab turgan BookingService ni ochib, uning konstruktorini va Reserve() ichini o'zgartirishimiz kerak bo'lardi, vaholanki bron qilish qoidalari o'zgarmagan. Bundan tashqari, testda emailni ataylab buzib bo'lmaydi, shuning uchun "email ketmasa ham bron yo'qolmaydi" degan qoidani isbotlab ham bo'lmasdi.

## Proof
- tests: refaktoringdan oldin ham, keyin ham 6 ta test o'tdi. R6 va SMS qo'shilgandan keyin 8 ta test o'tdi.
- demo: P03 dagi bilan bir xil, to'qqiz qatorning hammasi mos tushdi.
- race: hali ham double-booked (Confirmed reservations for R7 on 12-14 Nov: 2), ya'ni xatti-harakat o'zgarmagan.
