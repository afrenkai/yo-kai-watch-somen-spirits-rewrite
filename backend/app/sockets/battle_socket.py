import socketio
import json
import redis
from app.core.config import settings
from app.services.battle_engine import BattleEngine

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


active_battles = {}


def register_events(sio: socketio.AsyncServer):
    
    
    @sio.event
    async def connect(sid, environ):
        
        print(f"Client connected: {sid}")
        await sio.emit('connected', {'sid': sid}, to=sid)
    
    @sio.event
    async def disconnect(sid):
        print(f"Client disconnected: {sid}")
        
        for battle_id, battle_data in list(active_battles.items()):
            if sid in [battle_data.get('player1_sid'), battle_data.get('player2_sid')]:
                await sio.emit('opponent_disconnected', to=battle_data.get('player1_sid'))
                await sio.emit('opponent_disconnected', to=battle_data.get('player2_sid'))
                del active_battles[battle_id]
    
    @sio.event
    async def join_battle(sid, data):
        battle_id = data.get('battle_id')
        user_id = data.get('user_id')
        team_data = data.get('team')
        
        if not battle_id or not user_id:
            await sio.emit('error', {'message': 'Invalid battle data'}, to=sid)
            return
        
        if battle_id not in active_battles:
            active_battles[battle_id] = {
                'player1_sid': sid,
                'player1_id': user_id,
                'player1_team': team_data,
                'status': 'waiting'
            }
            await sio.emit('waiting_for_opponent', to=sid)
        else:
            battle = active_battles[battle_id]
            battle['player2_sid'] = sid
            battle['player2_id'] = user_id
            battle['player2_team'] = team_data
            battle['status'] = 'active'
            
            battle['engine'] = BattleEngine(
                battle['player1_team'],
                battle['player2_team']
            )

            await sio.emit('battle_start', {
                'opponent': {
                    'user_id': battle['player1_id'],
                    'team': battle['player1_team']
                }
            }, to=sid)
            
            await sio.emit('battle_start', {
                'opponent': {
                    'user_id': battle['player2_id'],
                    'team': battle['player2_team']
                }
            }, to=battle['player1_sid'])
            

            game_state = battle['engine'].get_state()
            await sio.emit('game_state', game_state, to=battle['player1_sid'])
            await sio.emit('game_state', game_state, to=battle['player2_sid'])
    
    @sio.event
    async def battle_action(sid, data):
        battle_id = data.get('battle_id')
        action = data.get('action')
        
        if battle_id not in active_battles:
            await sio.emit('error', {'message': 'Battle not found'}, to=sid)
            return
        
        battle = active_battles[battle_id]
        engine = battle.get('engine')
        
        if not engine:
            await sio.emit('error', {'message': 'Battle engine not initialized'}, to=sid)
            return
        
        player_num = 1 if sid == battle['player1_sid'] else 2
        
        result = engine.process_action(player_num, action)
        
        await sio.emit('action_result', result, to=battle['player1_sid'])
        await sio.emit('action_result', result, to=battle['player2_sid'])
        
        if engine.is_battle_over():
            winner = engine.get_winner()
            await sio.emit('battle_end', {'winner': winner}, to=battle['player1_sid'])
            await sio.emit('battle_end', {'winner': winner}, to=battle['player2_sid'])
            
            del active_battles[battle_id] # might need a better way to free this memory
        else:
            game_state = engine.get_state()
            await sio.emit('game_state', game_state, to=battle['player1_sid'])
            await sio.emit('game_state', game_state, to=battle['player2_sid'])
    
    @sio.event
    async def chat_message(sid, data):
        battle_id = data.get('battle_id')
        message = data.get('message')
        
        if battle_id not in active_battles:
            return
        
        battle = active_battles[battle_id]
        
        opponent_sid = battle['player2_sid'] if sid == battle['player1_sid'] else battle['player1_sid']
        await sio.emit('chat_message', {'message': message}, to=opponent_sid)
    
    return sio
