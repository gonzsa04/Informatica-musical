(

~joyaSound = Buffer.read(Server.default, "..//Sounds/crystalSound.wav");
~deathSound = Buffer.read(Server.default, "..//Sounds/deathSound.wav");
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
		Synth(\sampler, [\buffer, ~joyaSound]);
	},
	'/coge',
	nil,57120
);

OSCdef.new(
	\muere,
	{arg msg;
		Synth(\sampler, [\buffer, ~deathSound]);
	},
	'/muere',
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
	\degreePlay,
	{arg msg;

		//SCALES
		var scale;
		if(~paramsArray[2] == 0, {scale = Scale.major});
		if(~paramsArray[2] == 1, {scale = Scale.minor});
		if(~paramsArray[2] == 2, {scale = Scale.lydian});
		if(~paramsArray[2] == 3, {scale = Scale.ionian});
		if(~paramsArray[2] == 4, {scale = Scale.mixolydian});
		if(~paramsArray[2] == 5, {scale = Scale.dorian});
		if(~paramsArray[2] == 6, {scale = Scale.aeolian});
		if(~paramsArray[2] == 7, {scale = Scale.phrygian});
		if(~paramsArray[2] == 8, {scale = Scale.locrian});
		//SCALES

		Pbind(\degree, Pseq([~notesArray]), \dur, ~paramsArray[0], \amp, ~paramsArray[1] * msg[1], \scale, scale, \octave, ~paramsArray[3]).play;
		~notesArray = Array.new(~numNotes);
		~paramsArray = Array.new(~numParams);
	},
	'/degreePlay',
	nil,57120
);

OSCdef.new(
	\notePlay,
	{arg msg;

		//SCALES
		var scale;
		if(~paramsArray[2] == 0, {scale = Scale.major});
		if(~paramsArray[2] == 1, {scale = Scale.minor});
		if(~paramsArray[2] == 2, {scale = Scale.lydian});
		if(~paramsArray[2] == 3, {scale = Scale.ionian});
		if(~paramsArray[2] == 4, {scale = Scale.mixolydian});
		if(~paramsArray[2] == 5, {scale = Scale.dorian});
		if(~paramsArray[2] == 6, {scale = Scale.aeolian});
		if(~paramsArray[2] == 7, {scale = Scale.phrygian});
		if(~paramsArray[2] == 8, {scale = Scale.locrian});
		//SCALES

		Pbind(\note, Pseq([~notesArray]), \dur, ~paramsArray[0], \amp, ~paramsArray[1] * msg[1], \scale, scale, \octave, ~paramsArray[3]).play;
		~notesArray = Array.new(~numNotes);
		~paramsArray = Array.new(~numParams);
	},
	'/notePlay',
	nil,57120
);

)