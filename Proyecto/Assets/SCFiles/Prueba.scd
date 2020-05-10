(

~cogeVar = Buffer.read(Server.default, "D:/Users/Gonzalo/Desktop/UCM/1ro/MOTORES/Grupo28/Assets/Sounds/bShoot.wav");

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
		[msg].postln;

		Synth(\sampler, [\buffer, ~cogeVar]);
	},
	'/coge',
	nil,57120
);

)