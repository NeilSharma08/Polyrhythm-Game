import pygame, math
import time, sys, random, tkinter, json, os
from tkinter import ttk


bpm,polyrhythm,lc,sc,spc,uc,l=[None]*7

root = tkinter.Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="BPM:").grid(column=0, row=0)
bpme = ttk.Entry(frm)
bpme.grid(column=1, row=0)
ttk.Label(frm, text="Polyrhythm:").grid(column=0, row=1)
pe = ttk.Entry(frm)
pe.grid(column=1, row=1)
ttk.Label(frm, text="Line Color:").grid(column=0, row=2)
lce = ttk.Entry(frm)
lce.grid(column=1, row=2)
ttk.Label(frm, text="Square Color:").grid(column=0, row=3)
sce = ttk.Entry(frm)
sce.grid(column=1, row=3)
ttk.Label(frm, text="Approx. Square Color:").grid(column=0, row=4)
spce = ttk.Entry(frm)
spce.grid(column=1, row=4)
ttk.Label(frm, text="Usr Color:").grid(column=0, row=5)
uce = ttk.Entry(frm)
uce.grid(column=1, row=5)
ttk.Label(frm, text="Keys:").grid(column=0, row=6)
ke = ttk.Entry(frm)
ke.grid(column=1, row=6)

if (_i := os.path.isfile('pref.json')):
	try:
		j=json.loads((f:=open('pref.json')).read())
		bpme.insert(0,str(j['bpm']))
		pe.insert(0,str(j['p']))
		lce.insert(0,str(j['lc']))
		sce.insert(0,str(j['sc']))
		spce.insert(0,str(j['spc']))
		uce.insert(0,str(j['uc']))
		ke.insert(0,str(j['k']))
		f.close()
	except json.decoder.JSONDecodeError:
		pass
	except KeyError:
		pass

def go():
	global bpm, polyrhythm, lc, sc, spc, uc, k
	global bpme, pe, lce, sce, spce, usre, ke
	bpm = eval(bpme.get())
	polyrhythm = eval(pe.get())
	lc = eval(lce.get())
	sc = eval(sce.get())
	spc = eval(spce.get())
	uc = eval(uce.get())
	k = ke.get()
	
	f = open('pref.json', 'w')
	f.write(
		json.dumps({
			'bpm': bpm,
			'p': polyrhythm,
			'lc': lc,
			'sc': sc,
			'spc': spc,
			'uc': uc,
			'k': k
		})
	)
	f.close()
	
	root.destroy()
	
ttk.Button(frm, text="Go!", command=go).grid(column=1, row=7)
root.mainloop()



pygame.init()
sw, sh = 1280, 720
screen = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()
f = pygame.freetype.SysFont('Comic Sans MS', 30)
# lc = (0, 255, 0)
# sc = (0, 100, 0)
# spc = sc
# uc = (255, 0, 0)

# running = True
# tsst, trst  = f.render("")
# bst = pygame.Rect(sw / 2 - 50, sh / 2 - 25, 100, 50)
# while running:
	# for event in pygame.event.get():
		# if event.type == pygame.QUIT:
			# pygame.quit()
			# sys.exit(0)
		# elif event.type 

	# screen.fill("black")


dt = 0
# polyrhythm = (5, 6)
w = 2
lcm = 1
for i in polyrhythm:
	lcm = math.lcm(lcm, i)

wi = sw/lcm
# h = wi
if wi < sh / 8:
	wi = sh / 8
if wi > sh / 3:
	wi = sh / 3
	
h = sh / 8
wi = h
# bpm = 30
pps = lcm * wi * bpm / 60

print(pps)
if pps > 2000:
	wi = wi * (2000 / pps)
	pps = lcm * wi * bpm / 60

g = 20
gw = pps * g / 1000
cw = max(wi, gw)

# if pps > 50:
	# wi = wi / (polyrhythm[0] * polyrhythm[1])


running = True



def lgen():
	i = 0
	while True:
		yield ((
			i * wi,
			sh / 2 + h * (l/2)
		),
		(
			i * wi,
			sh / 2 - h * (l/2)
		))
		
		i += 1
		
def sygen(n):
	return tuple(sh / 2 + w/2 - h * (n/2 - i) for i in range(n))

def sgen(n):
	i = 0
	y = sygen(len(polyrhythm))
	#print(lcm)
	while True:
		yield pygame.Rect(
			i * wi * lcm / polyrhythm[n] + w/2,
			y[n],
			wi - w/2,
			h - w/2
		)
		i += 1
l = len(polyrhythm)
y = sygen(l)

# blines = (
	# ((0, sh / 2 - h), (sw, sh / 2 - h)),
	# ((0, sh / 2), (sw, sh / 2)),
	# ((0, sh / 2 + h), (sw, sh / 2 +h))
# )

blines = tuple(
	((0, sh / 2 - h * (i - l / 2)), (sw, sh / 2 - h * (i - l / 2))) for i in range(l+1)
)


lg = lgen()
sg = tuple(sgen(i)for i in range(len(polyrhythm)))

lines = list(next(lg)for i in range(int(sw / wi) + 2))
s = [list(next(sg[j])for i in range(int(sw / wi) + 1))for j in range(len(polyrhythm))]

# scan = pygame.Rect(sw / 2 - (wi - w) / 2, 0, wi - w, sh)
scan = pygame.Surface((cw - w, sh))
scan.set_alpha(128)
scan.fill((255,0,0))
# print(sw / 2 - (wi - w) / 2 )

# facci = (i.x for i in s_bot)
# jacci = (i.x for i in s_top)
# facc = list(facci)
# jacc = list(jacci)
acc = []
usr = []

camera = 0
p = 0
zag = pygame.Rect(sw - 5, sh / 6, 5, 5)
th = sh / 2 - h * l / 2 - 30

if not k:
	if l == 2:
		k = "jf"
	elif l == 3:
		k = "jkl"
	elif l == 4:
		k = "7890"
# start = time.time()

ur = pygame.Rect(0, th, sw, sh / 2 + h * l/2 - th + 1)
acc = []

while running:
	screen.fill("black")
	st = time.time() * 1000
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.unicode in k:
				usr.append(pygame.Rect(sw / 2 - (wi - w) / 2 + camera, y[k.find(event.unicode)], cw - w, h - w))
				for j in range(len(y)):
					if y[k.find(event.unicode)] == int(y[j]):
						acc.append(min(abs(sw / 2 - (wi - w) / 2 + camera - k.x) for k in s[j]))
				
				pass
		# print(event)
	
	st2 = time.time() * 1000	
	
	camera += dt * pps
	
	if lines[0][1][0] - camera < -wi:
		lines.append(next(lg))
		del lines[0]
	
	for i in range(len(polyrhythm)):
		if s[i][-1].x - camera < sw - wi:
			s[i].append(next(sg[i]))
		if s[i][0].x - camera < -wi:
			del s[i][0]
	
	# if s[0][0].x - camera < -wi:
		# del s[0][0]
	
	# if s[1][0].x - camera < -wi:
		# del s[1][0]
		# p += 1
		# if not p % polyrhythm[1]:
			# s_top.append(next(stg))
			# s_top.remove(s_top[0])
		# if not p % polyrhythm[0]:
			# s_bot.append(next(sbg))
			# s_bot.remove(s_bot[0])
	st3 = time.time() * 1000
	
	if usr and usr[0].x - camera <= -wi:	
		usr.remove(usr[0])
		acc.remove(acc[0])
	
	zag.move_ip(-1, 0)
	
	st4 = time.time() * 1000
	
	for i in blines:
		pygame.draw.line(screen, lc, i[0], i[1], width = w)
	
	for j in s:
		for i in j:
			pygame.draw.rect(screen, sc, i.move(-camera, 0))
	# for i in s[0]:
		# pygame.draw.rect(screen, sc, i.move(-camera,0))
	
	# for i in s[1]:
		# pygame.draw.rect(screen, spc, pygame.Rect((_i:=i.move(-camera, 0)).x + _i.w/2 - gw / 2, i.y, gw, h - w/2))
		# pygame.draw.rect(screen, sc, i.move(-camera,0))
	
	for i in lines:
		pygame.draw.line(screen, lc, (i[1][0] - camera, i[1][1]), (i[0][0] - camera, i[0][1]), width = w)
	
	for j in s:
		for i in j:
			pygame.draw.rect(screen, spc, pygame.Rect((_i:=i.move(-camera, 0)).x + _i.w/2 - gw / 2, i.y, gw, h - w/2))
	
	# for i in s[1]:
		# pygame.draw.rect(screen, spc, pygame.Rect((_i:=i.move(-camera, 0)).x + _i.w/2 - gw / 2, i.y, gw, h - w/2))
	
	
	screen.blit(scan, (sw / 2 - (wi - w) / 2, 0))
	st5 = time.time() * 1000
	# acc = []
	for i in usr:
		# print(i.y)
		# print(sh/2 - h + w/2)
		# for j in range(len(y)):
			# if i.y == int(y[j]):
				# acc.append(min(abs(i.x - k.x) for k in s[j]))
		# if i.y == int(sh/2 - h + w/2):
			# print("h")
			# acc.append(min(abs(i.x - j.x) for j in s[0]))
		# else:
			# acc.append(min(abs(i.x - j.x) for j in s[1]))
		pygame.draw.rect(screen, uc, i.move(-camera,0))
	
	ts, tr = f.render("Error:  " + (str(round(1000 * sum(acc)/len(acc)/pps,0)) + " ms" if acc else "NaN"), (255, 255, 255))
	screen.blit(ts, (sw/2 - tr.width/2, th))
	# tst, trt = f.render("Time: " + str(round(time.time() - start, 2)), (255,255,255))
	# screen.blit(tst, (sw/2 - trt.width/2, th - 50))
	st6 = time.time() * 1000
	
	print(
		round(st6 - st5, 0),
		round(st5 - st4, 0),
		round(st4 - st3, 0),
		round(st3 - st2, 0),
		round(st2 - st, 0)) if st6 - st > 1000 * 1/120 else ()
	dt = clock.tick(9999) / 1000	
	pygame.display.update(ur)
	
pygame.quit()