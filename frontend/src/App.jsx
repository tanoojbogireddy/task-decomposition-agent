import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [goal, setGoal] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!goal.trim()) return;

    setMessages(prev => [...prev, { type: 'user', text: goal }]);
    setGoal('');
    setLoading(true);

    try {
      setMessages(prev => [...prev, { type: 'thinking' }]);
      
      const response = await axios.post('http://127.0.0.1:8000/execute', {
        goal: goal
      });

      setMessages(prev => prev.filter(m => m.type !== 'thinking'));
      setMessages(prev => [...prev, { type: 'tasks', tasks: response.data.tasks }]);
      setMessages(prev => [...prev, { type: 'answer', text: response.data.final_answer, time: response.data.time_taken }]);
    } catch (err) {
      setMessages(prev => prev.filter(m => m.type !== 'thinking'));
      setMessages(prev => [...prev, { type: 'error', text: err.message }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-header">
              <div className="title-badge">
                <h1>Task Architect</h1>
              </div>
              <p>Turn goals into executable tasks</p>
            </div>

            <div className="examples">
              <button className="example-card" onClick={() => setGoal('Write a report on renewable energy')}>
                <span className="example-emoji"></span>
                <span className="example-text">Write a report</span>
              </button>
              <button className="example-card" onClick={() => setGoal('Analyze market data')}>
                <span className="example-emoji"></span>
                <span className="example-text">Analyze market</span>
              </button>
              <button className="example-card" onClick={() => setGoal('Create a business plan')}>
                <span className="example-emoji"></span>
                <span className="example-text">Create strategy</span>
              </button>
            </div>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((msg, idx) => (
              <div key={idx} className={`msg msg-${msg.type}`}>
                {msg.type === 'user' && (
                  <div className="msg-bubble user">
                    {msg.text}
                  </div>
                )}

                {msg.type === 'thinking' && (
                  <div className="msg-bubble thinking">
                    <span className="dot"></span>
                    <span className="dot"></span>
                    <span className="dot"></span>
                  </div>
                )}

                {msg.type === 'tasks' && (
                  <div className="msg-bubble tasks">
                    {msg.tasks.map(task => (
                      <div key={task.id} className="task">
                        <div className="task-num">{task.id}</div>
                        <div className="task-info">
                          <div className="task-title">{task.description}</div>
                          <div className="task-tools">
                            {task.tools.join(' • ')}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {msg.type === 'answer' && (
                  <div className="msg-bubble answer">
                    <div className="answer-content">
                      {msg.text}
                    </div>
                    <div className="answer-time">
                      ⏱️ {msg.time.toFixed(2)}s
                    </div>
                  </div>
                )}

                {msg.type === 'error' && (
                  <div className="msg-bubble error">
                    ⚠️ {msg.text}
                  </div>
                )}
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>
        )}
      </div>

      <div className="input-container">
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="What would you like to accomplish?"
            disabled={loading}
          />
          <button type="submit" disabled={loading || !goal.trim()}>
            {loading ? <span className="spinner"></span> : '→'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;