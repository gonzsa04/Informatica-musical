(

~kkVar = Buffer.read(Server.default, "D:/Users/Gonzalo/Desktop/UCM/1ro/MOTORES/Grupo28/Assets/Sounds/bShoot.wav");
~numNotes = 5;
~notesArray = Array.new(~numNotes);
~numParams = 5;
~paramsArray = Array.new(~numParams);

SynthDef(\sampler, {
	arg out = 0, rate = 1, amp = 0.5, buffer = 0;
	var signal;

	signal =
	PlayBuf.ar(1, buffer,
		BufRateScale.kr(buffer)*rate,
		doneAction:2
	);

	Out.ar(out, signal!2 * amp);

}).add;

OSCdef.new(
	\coge,
	{arg msg;
		//[msg].postln;

		Synth(\sampler, [\buffer, ~kkVar]);
	},
	'/coge',
	nil,57120
);

OSCdef.new(
	\loadNote,
	{arg msg;
		~notesArray.add(msg[1]);
	},
	'/loadNote',
	nil,57120
);

OSCdef.new(
	\loadParams,
	{arg msg;
		~paramsArray.add(msg[1]);
	},
	'/loadParams',
	nil,57120
);

OSCdef.new(
	\play,
	{arg msg;
		//msg[1].postln;
		var scale;
		if(~paramsArray[2] == 0, {scale = Scale.major}, {scale = Scale.minor});

		Pbind(\degree, Pseq([~notesArray]), \dur, ~paramsArray[0], \amp, ~paramsArray[1], \scale, scale, \octave, ~paramsArray[3]).play;
		~notesArray = Array.new(~numNotes);
		~paramsArray = Array.new(~numParams);
	},
	'/play',
	nil,57120
);

)