(function()
{
	function switchImage(e)
	{
		document.querySelector('.images .selected').classList.remove('selected');
		e.currentTarget.classList.add('selected');
		document.getElementById('viewer').src = e.currentTarget.src;
	}
	const allImages = document.querySelectorAll('.images img');
	allImages[0].classList.add('selected');
	for (let img of allImages)
		img.addEventListener('click', switchImage);
	function switchSize(e)
	{
		try
		{
			document.querySelector('#sizes .selected').classList.remove('selected');
		}
		catch(err)
		{
			if (err instanceof TypeError)
				;
			else
				throw err;
		}
		e.currentTarget.classList.add('selected');
	}
	const allSizes = document.querySelectorAll('#sizes li');
	for (let size of allSizes)
		size.addEventListener('click', switchSize);
	function switchColor(e)
	{
		try
		{
			document.querySelector('#colors .selected').classList.remove('selected');
		}
		catch(err)
		{
			if (err instanceof TypeError)
				;
			else
				throw err;
		}
		e.currentTarget.classList.add('selected');
	}
	const allColors = document.querySelectorAll('#colors li');
	for (let color of allColors)
		color.addEventListener('click', switchColor);
})();