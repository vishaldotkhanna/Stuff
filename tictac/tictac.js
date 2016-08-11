var player, mark, move, state, turn; 
var board = document.getElementsByClassName('board')[0];
var map = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]];

window.onload = function()	{
	player = 0;
	mark = 'O';
	move = 0;
	state = [0, 0, 0, 0, 0, 0, 0, 0, 0];
	turn = document.getElementById('player-indicator');	

	for(var j = 0;j < 3;j++)	{
		for(var k = 0;k < 3;k++)	{
			board.rows[j].cells[k].onclick = function()	{
				var index = this.cellIndex + 3 * this.parentNode.rowIndex;

				if (move < 9 && state[index] == 0)	{
					this.innerHTML = mark;
					
					if(!player)
						state[index] = 1;
					else
						state[index] = 2;

					update_state();
					check_result();

					if(move == 8)	{
						window.alert("It's a draw!");	
						location.reload();
					}

					move++;
				}
				else    {
					console.log('Unattended case');
				}
			}
		}
	}


}

function update_state()    {
	player = (player + 1) % 2;

	if(!player)	{
		mark = 'O';
		turn.innerHTML = "1's";
	}			
	else	{
		mark = 'X';
		turn.innerHTML = "2's";
	}

}

function delay(p)	{
	window.alert('Player ' + p + ' wins!');
	location.reload();
}

function check_result()	{

	if(state[0] == state[3] && state[3] == state[6] && state[0] != 0)	{
		change_color(0, 3, 6);
		setTimeout(delay(state[0]), 1000);
	}

	else if(state[1] == state[4] && state[4] == state[7] && state[1] != 0)	{
		change_color(1, 4, 7);
		setTimeout(delay(state[1]), 1000);
	}

	else if(state[2] == state[5] && state[5] == state[8] && state[2] != 0)	{
		change_color(2, 5, 8);
		setTimeout(delay(state[2]), 1000);
	}

	else if(state[0] == state[1] && state[1] == state[2] && state[0] != 0)	{
		change_color(0, 1, 2);
		setTimeout(delay(state[0]), 1000);
	}

	else if(state[3] == state[4] && state[4] == state[5] && state[3] != 0)	{
		change_color(3, 4, 5);
		setTimeout(delay(state[3]), 1000);
	}

	else if(state[6] == state[7] && state[7] == state[8] && state[6] != 0)	{
		change_color(6, 7, 8);
		setTimeout(delay(state[6]), 1000);
	}

	else if(state[0] == state[4] && state[4] == state[8] && state[0] != 0)	{
		change_color(0, 4, 8);
		setTimeout(delay(state[4]), 1000);
	}

	else if(state[2] == state[4] && state[4] == state[6] && state[2] != 0)	{
		change_color(2, 4, 6);
		setTimeout(delay(state[2]), 1000);
	}
}

function change_color(i, j, k)	{
	console.log('In delay');
	for(var l = 0;l < arguments.length;l++)    {
		var temp = arguments[l];
		board.rows[map[temp][0]].cells[map[temp][1]].style['backgroundColor'] = '#F1991A';
	}
}



